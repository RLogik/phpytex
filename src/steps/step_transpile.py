#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import src.paths;

from src.thirdparty.maths import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;
from src.thirdparty.system import *;

from src.setup import *;
from src.core.log import *;
from src.core.utils import *;
from src.models.internal import *;
from src.models.config import *;
from src.models.user import *;
from src.parsers import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'step_transpile',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOCAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

exportvars = dict();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step transpile phpytex to python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step_transpile():
    global exportvars;
    log_info('TRANSPILATION (phpytex -> python) STARTED.');
    options = config.TRANSPILATION;
    config.PATHS.file_stamp

    # only do this once!
    reseed(options.seed);

    ## Initialise structures for recording transpilation units:
    preambles = [];
    exportvars = dict();
    imports = TranspileBlocks();
    documents = TranspileDocuments(
        root = src.paths.wd,
        indent_symbol = options.indent_symbol,
        name_space = config.NAMESPACE,
    );

    ## Transpile preamble:
    if config.PATHS.file_stamp is not None:
        options_ = options.copy();
        options_.comments = EnumCommentsOption.on;
        options_.show_tree = False;
        name = 'stamp';
        preambles.append(name);
        transpile_preamble(
            name = name,
            path = config.PATHS.file_stamp,
            documents = documents,
            imports = TranspileBlocks(),
            options = options_,
        );

    ## Transpile document file:
    transpile_document(
        path = config.PATHS.file_start,
        documents = documents,
        options = options,
        imports = imports,
        silent = get_quiet_mode(),
    );

    ## Add document structure:
    name = 'tree';
    if options.show_tree:
        preambles.append(name);
    blocks = TranspileBlocks([create_block_tree(documents, seed=options.seed)]);
    documents.append_preamble(name=name, blocks=blocks);

    ## Handle global parameters:
    if config.PATHS.file_params_py is not None:
        ## Create file:
        create_import_file_parameters(
            path      = os.path.join(sys.path.wd, config.PATHS.file_params_py),
            overwrite = config.PATHS.overwrite_params,
            documents = documents
        );
        ## Add import block for global parameters:
        imports.append(TranspileBlock(
            kind        = 'code',
            content     = f'from {config.PATHS.import_params} import *;',
            level       = 0,
            indent_symbol  = options.indent_symbol,
        ));

    ## Generate result of transpilation (phpytex -> python):

    globalvars = unique(list(exportvars.keys()) + list(documents.variables.keys()));
    create_metacode(
        documents  = documents,
        imports    = imports,
        preambles  = preambles,
        globalvars = globalvars,
    );

    log_info('TRANSPILATION (phpytex -> python) COMPLETE.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def transpile_preamble(
    name: str,
    path: str,
    documents: TranspileDocuments,
    options: TranspileOptions,
):
    try:
        lines = read_text_file(path);
    except:
        log_error(f'Could not find or read document \x1b[1m{path}\x1b[0m!');
        return;

    indentation = IndentationTracker(
        symbol = options.indent_symbol,
        pattern = options.indent_symbol_re,
    );

    blocks = TranspileBlocks();
    for block in parseText(lines, indentation, offset=options.offset_symbol):
        if (block.kind, block.sub_kind) == (EnumTokenisationBlockKind.text, EnumTokenisationBlockSubKind.comment):
            blocks.append(block);
    blocks.append(TranspileBlock(
        kind = EnumTokenisationBlockKind.text,
        sub_kind = EnumTokenisationBlockSubKind.empty,
        level = 0,
        indent_symbol = documents.indent_symbol,
    ));
    documents.append_preamble(name=name, blocks=blocks);
    log_plain(display_tree_branch(path=path));
    return;

def transpile_document(
    path: str,
    documents: TranspileDocuments,
    options: TranspileOptions,
    imports: TranspileBlocks,
    silent: bool = False,
    chain: list[str] = [],
):
    if path in chain:
        log_error('The document contains a cycle!');
        return;
    if path in documents.paths:
        return;

    try:
        lines = read_text_file(path);
    except:
        log_error(f'Could not find or read document \x1b[1m{path}\x1b[0m!');
        return;

    depth = len(chain);
    indentation = IndentationTracker(
        symbol = options.indent_symbol,
        pattern = options.indent_symbol_re,
    );

    # NOTE: need to add document first, in order to update anon- + hide-state:
    document = documents.append_document(path=path);
    anon = documents.anon[path];
    hide = documents.hide[path];

    blocks = TranspileBlocks();

    if not silent:
        log_plain(display_tree_branch(path=path, anon=anon, depth=depth));

    if options.show_tree:
        blocks.append(create_block_stamp(documents, depth=0, start=True, anon=anon, hide=hide));

    for block in parseText(lines, indentation, offset=options.offset_symbol):
        match (block.kind, block.sub_kind):
            case (EnumTokenisationBlockKind.code, EnumTokenisationBlockSubKind.import_):
                imports.append(block);
            case (EnumTokenisationBlockKind.text, EnumTokenisationBlockSubKind.comment):
                match options.comments:
                    case EnumCommentsOption.auto:
                        if block.parameters.keep:
                            blocks.append(block);
                    case EnumCommentsOption.on | EnumCommentsOption.true:
                        blocks.append(block);
                    case _:
                        pass;
            case _:
                blocks.append(block);

    if options.show_tree:
        blocks.append(create_block_stamp(documents, depth=0, start=False, anon=anon, hide=hide));

    # add transpiled blocks to document:
    documents.append_blocks(document, blocks=blocks);

    # call recursively for subpaths:
    for subpath in documents.subpaths(path):
        transpile_document(
            path = subpath,
            documents = documents,
            options = options,
            imports = imports,
            silent = silent,
            chain = chain + [path],
        );
    return;

def create_import_file_parameters(
    path: str,
    overwrite: bool,
    documents: TranspileDocuments
):
    global exportvars;

    if os.path.exists(path) and not overwrite:
        return;

    lines = dedent_as_list(
        '''
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-
        '''
    );
    lines.append('');

    names = exportvars.keys();
    for name, (value, codedvalue) in exportvars.items():
        lines.append('{name} = {codedvalue};'.format(name=name, codedvalue=codedvalue));

    for name in documents.variables.keys():
        if name in names:
            continue;
        lines.append('{name} = None;'.format(name=name));
    lines.append('');

    write_text_file(path=path, lines=lines, force_create_path=True);

    return;

def create_metacode(
    documents: TranspileDocuments,
    imports: TranspileBlocks,
    preambles: list[str],
    globalvars: list[str],
):
    options = config.TRANSPILATION;
    _lines_pre = assets.TEMPLATE_PHPYTEX_LINES_PRE;
    _lines_post = assets.TEMPLATE_PHPYTEX_LINES_POST;
    lines = [];
    lines += dedent_as_list(
        _lines_pre.format(
            imports = '\n'.join(imports.to_code()),
            root = src.paths.wd,
            output = os.path.join(src.paths.wd, options.output),
            name = options.output,
            insert_bib = options.insert_bib,
            compile_latex = options.compile_latex,
            length_max = options.max_length,
            seed = options.seed,
            indent_symbol = options.indent_symbol,
            censor_symbol = options.censor_symbol,
            mainfct = config.NAMESPACE.function_name_main,
        )
    );
    lines.append('');
    lines += documents.to_code(offset=0, preambles=preambles, globalvars=globalvars);
    lines.append('');
    lines += dedent_as_list(_lines_post.format());
    write_text_file(config.PATHS.file_transpiled, lines);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def display_tree_branch(
    path: str,
    anon: bool = False,
    prefix: str = '',
    indent_symbol: str = '    ',
    branchsymb: str = '  |____ ',
    depth: int = 0,
) -> str:
    options = config.TRANSPILATION;
    return '{prefix}{tab}{branchsymb}{path}'.format(
        prefix = prefix,
        tab = indent_symbol * max(depth - 1, 0),
        branchsymb = ' ' if depth == 0 else branchsymb,
        path = options.censor_symbol if anon else path,
    );
