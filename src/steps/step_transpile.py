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
        indentsymb = options.indent_character,
        name_space = config.NAMESPACE,
    );

    ## Transpile preamble:
    if config.PATHS.file_stamp is not None:
        options_ = options.copy();
        options_.comments = EnumCommentsOption.on;
        options_.show_tree = False;
        name = 'stamp';
        preambles.append(name);
        transpile_document(
            path        = config.PATHS.file_stamp,
            documents   = documents,
            imports     = TranspileBlocks(),
            name        = name,
            is_preamble = True,
            silent      = True,
            options     = options_,
        );

    ## Transpile document file:
    transpile_document(
        path        = config.PATHS.file_start,
        documents   = documents,
        imports     = imports,
        name        = '',
        is_preamble = False,
        silent      = get_quiet_mode(),
        options     = options,
    );

    ## Add document structure:
    name = 'tree';
    if options.show_tree:
        preambles.append(name);
    blocks = TranspileBlocks([documents.documentTree(seed=options.seed)]);
    documents.addPreamble(name=name, blocks=blocks);

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
            indentsymb  = options.indent_character,
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

def transpile_document(
    path: str,
    documents: TranspileDocuments,
    imports: TranspileBlocks,
    options: TranspileOptions,
    chain: list[str] = [],
    name: str = '',
    is_preamble: bool = False,
    silent: bool = False,
):
    if path in chain:
        log_error('The document contains a cycle!');
        return;
    try:
        lines = read_text_file(path);
    except:
        log_error('Could not find or read document \033[1m{path}\033[0m!'.format(path = path));
        return;
    depth = len(chain);
    indentsymb = options.indent_character;
    offset = options.offset_symbol;
    indentation = IndentationTracker(
        symb    = indentsymb,
        pattern = options.indent_character_re,
    );

    # cases 1+2:
    if is_preamble:
        blocks = TranspileBlocks();

        for block in parseText(lines, indentation, offset=offset):
            if block.kind == 'text:comment':
                blocks.append(block);

        blocks.append(TranspileBlock(kind='text:empty'))

        documents.addPreamble(name=name, blocks=blocks);
        log_plain(display_tree_branch(path=path, anon=False, depth=depth));
        return;
    elif path in documents.paths:
        return;

    # case 3:

    # NOTE: need to do this first, in order to update anon-state
    documents.addDocument(path=path);
    anon = documents.isAnon(path=path);
    hide = documents.isHidden(path=path);
    blocks = TranspileBlocks();
    log_plain(display_tree_branch(path=path, anon=anon, depth=depth));

    if options.show_tree:
        blocks.append(documents.documentStamp(depth=0, start=True, anon=anon, hide=hide));

    for block in parseText(lines, indentation, offset=offset):
        match block.kind:
            case 'code:import':
                imports.append(block);
            case 'text:comment':
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
        blocks.append(documents.documentStamp(depth=0, start=False, anon=anon, hide=hide));

    documents.addBlocks(path=path, blocks=blocks);
    for subpath in documents.subpaths(path):
        transpile_document(
            path      = subpath,
            documents = documents,
            imports   = imports,
            chain     = chain + [path],
            silent    = silent,
            options   = options,
        );
    return;

def create_import_file_parameters(
    path: str,
    overwrite: bool,
    documents: TranspileDocuments
):
    global exportvars;
    options = config.TRANSPILATION;

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
            imports       = '\n'.join(imports.generateCode()),
            root          = src.paths.wd,
            output        = os.path.join(src.paths.wd, options.output),
            name          = options.output,
            insert_bib    = options.insert_bib,
            compile_latex = options.compile_latex,
            length_max    = options.max_length,
            seed          = options.seed,
            indentsymb    = options.indent_character,
            censorsymb    = options.censor_symbol,
            mainfct       = config.NAMESPACE.function_name_main,
        )
    );
    lines.append('');
    lines += documents.generateCode(offset=0, preambles=preambles, globalvars=globalvars);
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
    indentsymb: str = '    ',
    branchsymb: str = '  |____ ',
    depth: int = 0,
) -> str:
    options = config.TRANSPILATION;
    return '{prefix}{tab}{branchsymb}{path}'.format(
        prefix = prefix,
        tab = indentsymb * max(depth - 1, 0),
        branchsymb = ' ' if depth == 0 else branchsymb,
        path = options.censor_symbol if anon else path,
    );
