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
from src.models.user import *;
from src.parsers import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'step_transpile',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step transpile phpytex to python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step_transpile():
    log_info('TRANSPILATION (phpytex -> python) STARTED.');
    indentsymb = config.TRANSPILATION.indent_character;

    # only do this once!
    seed = config.TRANSPILATION.seed;
    reseed(seed);
    return;

    ## Initialise structures for recording transpilation units:
    preambles = [];
    imports = TranspileBlocks();
    documents = TranspileDocuments(
        root       = src.paths.wd,
        indentsymb = indentsymb,
        schemes    = dict(
            file = config.NAMESPACE. FUNCTION_NAME_FILE,
            main = config.NAMESPACE. FUNCTION_NAME_MAIN,
            pre  = config.NAMESPACE. FUNCTION_NAME_PRE
        )
    );
    return;

    ## Transpile preamble:
    if appconfig.getWithFileStamp():
        name = 'stamp';
        preambles.append(name);
        transpileDocument(
            path        = appconfig.getFileStamp(rel=True),
            documents   = documents,
            imports     = TranspileBlocks(),
            name        = name,
            is_preamble = True,
            silent      = True,
            params      = { 'comm': True, 'comm-auto': False, 'show-tree': False }
        );

    ## Transpile document file:
    transpileDocument(
        path        = appconfig.getFileStart(rel=True),
        documents   = documents,
        imports     = imports,
        name        = '',
        is_preamble = False,
        silent      = get_quiet_mode(),
        params      = {
            'comm':      appconfig.getOptionCommentsOn(),
            'comm-auto': appconfig.getOptionCommentsAuto(),
            'show-tree': appconfig.getOptionShowTree()
        }
    );

    ## Add document structure:
    name = 'tree';
    if appconfig.getOptionShowTree():
        preambles.append(name);
    blocks = TranspileBlocks([documents.documentTree(seed=seed)]);
    documents.addPreamble(name=name, blocks=blocks);

    ## Handle global parameters:
    if appconfig.getWithFileParamsPy():
        ## Create file:
        createImportFileParameters(
            path      = appconfig.getFileParamsPy(rel=False),
            overwrite = appconfig.getOptionOverwriteParams(),
            documents = documents
        );
        ## Add import block for global parameters:
        imports.append(TranspileBlock(
            kind        = 'code',
            content     = 'from {name} import *;'.format(name = appconfig.getImportParamsPy()),
            level       = 0,
            indentsymb  = indentsymb,
        ));

    ## Generate result of transpilation (phpytex -> python):
    globalvars = unique(list(appconfig.getExportVars().keys()) + list(documents.variables.keys()));
    createmetacode(
        documents  = documents,
        imports    = imports,
        preambles  = preambles,
        globalvars = globalvars,
        seed       = seed
    );
    log_info('TRANSPILATION (phpytex -> python) COMPLETE.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def transpileDocument(
    path:         str,
    documents:    TranspileDocuments,
    imports:      TranspileBlocks,
    chain:        list[str]          = [],
    name:         str                = '',
    is_preamble:  bool               = False,
    silent:       bool               = False,
    params:       dict[str, bool]    = dict()
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
    indentsymb = appconfig.getIndentCharacter();
    offset = appconfig.getOffsetSymbol();
    indentation = IndentationTracker(
        symb    = indentsymb,
        pattern = appconfig.getIndentCharacterRe(),
    );

    if is_preamble:
        blocks = TranspileBlocks();
        for block in parseText(lines, indentation, offset=offset):
            if not (block.kind == 'text:comment'):
                continue;
            blocks.append(block);
        blocks.append(TranspileBlock(kind='text:empty'))
        documents.addPreamble(name=name, blocks=blocks);
        log_plain(displayTreeBranch(path=path, anon=False, depth=depth));
    else:
        if path in documents.paths:
            return;
        documents.addDocument(path=path); ## NOTE: need to do this first, in order to update anon-state
        anon = documents.isAnon(path=path);
        hide = documents.isHidden(path=path);
        blocks = TranspileBlocks();
        log_plain(displayTreeBranch(path=path, anon=anon, depth=depth));

        if params['show-tree']:
            blocks.append(documents.documentStamp(depth=0, start=True, anon=anon, hide=hide));
        for block in parseText(lines, indentation, offset=offset):
            if block.kind == 'code:import':
                imports.append(block);
                continue;
            if block.kind == 'text:comment':
                if params['comm-auto'] == True:
                    if not block.parameters.keep:
                        continue;
                elif params['comm'] == False:
                    continue;
            blocks.append(block);
        if params['show-tree']:
            blocks.append(documents.documentStamp(depth=0, start=False, anon=anon, hide=hide));

        documents.addBlocks(path=path, blocks=blocks);
        for subpath in documents.getSubPaths(path):
            transpileDocument(
                path      = subpath,
                documents = documents,
                imports   = imports,
                chain     = chain + [path],
                silent    = silent,
                params    = params
            );
    return;

def createImportFileParameters(
    path:      str,
    overwrite: bool,
    documents: TranspileDocuments
):
    if os.path.exists(path) and not overwrite:
        return;
    lines = dedent_as_list(
        '''
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-
        '''
    );
    lines.append('');
    names = appconfig.getExportVars().keys();
    for name, (value, codedvalue) in appconfig.getExportVars().items():
        lines.append('{name} = {codedvalue};'.format(name=name, codedvalue=codedvalue));
    for name in documents.variables.keys():
        if name in names:
            continue;
        lines.append('{name} = None;'.format(name=name));
    lines.append('');
    write_text_file(path=path, lines=lines, force_create_path=True);
    return;

def createmetacode(
    options: UserTranspileOptions,
    documents:  TranspileDocuments,
    imports:    TranspileBlocks,
    preambles:  list[str],
    globalvars: list[str],
    seed:       Optional[int]
):
    _lines_pre = get_template_phpytex_lines_pre();
    _lines_post = get_template_phpytex_lines_post();
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
            indentsymb    = appconfig.getIndentCharacter(),
            censorsymb    = appconfig.getCensorSymbol(),
            mainfct       = config.FUNCTION_NAME_MAIN,
        )
    );
    lines.append('');
    lines += documents.generateCode(offset=0, preambles=preambles, globalvars=globalvars);
    lines.append('');
    lines += dedent_as_list(
        _lines_post.format()
    );
    write_text_file(appconfig.getFileTranspiled(rel=False), lines);
    return;

def displayTreeBranch(
    path:       str,
    anon:       bool = False,
    prefix:     str  = '',
    indentsymb: str  = '    ',
    branchsymb: str  = '  |____',
    depth:      int  = 0
) -> str:
    return '{prefix}{tab}{branchsymb} {path}'.format(
        prefix = prefix,
        tab = indentsymb*(depth if depth == 0 else depth - 1),
        branchsymb = '' if depth == 0 else branchsymb,
        path = appconfig.getCensorSymbol() if anon else path,
    );
