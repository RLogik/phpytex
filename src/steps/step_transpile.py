#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.maths import *;
from src.local.typing import *;

from src.core.log import *;
from src.core.utils import formatTextBlockAsList;
from src.core.utils import readTextFile;
from src.core.utils import unique;
from src.core.utils import writeTextFile;
from src.customtypes.exports import *;
from src.setup import appconfig;
from src.setup.methods import getTemplatePhpytexLinesPre;
from src.setup.methods import getTemplatePhpytexLinesPost;
from src.setup.templates.exports import *;
from src.parsers.phpytex import parseText;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step transpile phpytex to python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step():
    logInfo('TRANSPILATION (phpytex -> python) STARTED.');
    root = appconfig.getPathRoot();
    indentsymb = appconfig.getIndentCharacter();

    ## Initialise structures for recording transpilation units:
    random.seed(appconfig.getSeed()); # <-- only do this once!
    preambles = [];
    imports = TranspileBlocks();
    documents = TranspileDocuments(
        root       = root,
        indentsymb = indentsymb,
        schemes    = dict(
            file = FUNCTION_NAME_FILE,
            main = FUNCTION_NAME_MAIN,
            pre  = FUNCTION_NAME_PRE
        )
    );

    ## Transpile preamble:
    name = 'stamp';
    preambles.append(name);
    transpileDocument(
        path        = appconfig.getFileStamp(rel=True),
        documents   = documents,
        imports     = TranspileBlocks(),
        name        = name,
        is_preamble = True,
        silent      = True,
        params      = { 'no-comm': False, 'no-comm-auto': True, 'show-tree': False }
    );

    ## Transpile document file:
    transpileDocument(
        path        = appconfig.getFileStart(rel=True),
        documents   = documents,
        imports     = imports,
        name        = '',
        is_preamble = False,
        silent      = getQuietMode(),
        params      = {
            'no-comm':      (appconfig.getOptionComments() is False),
            'no-comm-auto': (appconfig.getOptionComments() == 'auto'),
            'show-tree':    appconfig.getOptionShowTree()
        }
    );

    ## Add document structure:
    name = 'tree';
    if appconfig.getOptionShowTree():
        preambles.append(name);
    blocks = TranspileBlocks([documents.documentTree(seed=appconfig.getSeed())]);
    documents.addPreamble(name=name, blocks=blocks);

    ## Create `parameters.py`:
    createImportFileParameters(
        path      = appconfig.getFileParamsPy(rel=False),
        overwrite = appconfig.getOptionOverwriteParams(),
        documents = documents
    );

    ## Add import block for global parameters:
    imports.append(TranspileBlock(
        kind        = 'code',
        content     = 'from {name} import *;'.format(name = appconfig.getImportParamsPy()),
        indentlevel = 0,
        indentsymb  = indentsymb,
    ));

    ## Generate result of transpilation (phpytex -> python):
    globalvars = unique(list(appconfig.getExportVars().keys()) + list(documents.variables.keys()));
    createmetacode(
        documents  = documents,
        imports    = imports,
        preambles  = preambles,
        globalvars = globalvars
    );
    logInfo('TRANSPILATION (phpytex -> python) COMPLETE.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def transpileDocument(
    path:         str,
    documents:    TranspileDocuments,
    imports:      TranspileBlocks,
    chain:        List[str]          = [],
    name:         str                = '',
    is_preamble:  bool               = False,
    silent:       bool               = False,
    params:       Dict[str, bool]    = dict()
):
    if path in chain:
        logError('The document contains a cycle!');
        return;
    try:
        lines = readTextFile(path);
    except:
        logError('Could not find or read document \033[1m{path}\033[0m!'.format(path = path));
        return;
    depth = len(chain);
    indentsymb = appconfig.getIndentCharacter();
    indentation = IndentationTracker(
        symb       = indentsymb,
        pattern    = appconfig.getIndentCharacterRe(),
        is_legacy  = appconfig.getOptionLegacy(),
    );

    logPlain(displayTreeBranch(path=path, anon=documents.isAnon(path), depth=depth));

    if is_preamble:
        blocks = TranspileBlocks();
        for block in parseText(lines, indentation):
            if not (block.kind == 'text:comment'):
                continue;
            blocks.append(block);
        blocks.append(TranspileBlock(kind='text:empty'))
        documents.addPreamble(name=name, blocks=blocks);
    else:
        if path in documents.paths:
            return;
        documents.addDocument(path=path); ## NOTE: need to do this first, in order to update anon-state
        blocks = TranspileBlocks();
        if params['show-tree']:
            blocks.append(documents.documentStamp(depth=0, start=True));
        for block in parseText(lines, indentation):
            if block.kind == 'code:import':
                imports.append(block);
                continue;
            if block.kind == 'text:comment':
                if params['no-comm'] or ( params['no-comm-auto'] and not block.parameters.keep ):
                    continue;
            blocks.append(block);
        if params['show-tree']:
            blocks.append(documents.documentStamp(depth=0, start=False));
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
    lines = formatTextBlockAsList(
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
    writeTextFile(path=path, lines=lines, force_create_path=True);
    return;

def createmetacode(
    documents:  TranspileDocuments,
    imports:    TranspileBlocks,
    preambles:  List[str],
    globalvars: List[str]
):
    fnameLatex = appconfig.getFileOutput(rel=False);
    _lines_pre = getTemplatePhpytexLinesPre();
    _lines_post = getTemplatePhpytexLinesPost();
    lines = [];
    lines += formatTextBlockAsList(
        _lines_pre.format(
            imports       = '\n'.join(imports.generateCode()),
            root          = appconfig.getPathRoot(),
            output        = appconfig.getFileOutput(rel=False),
            name          = appconfig.getFileOutputBase(),
            insert_bib    = appconfig.getOptionInsertBib(),
            compile_latex = appconfig.getOptionCompileLatex(),
            length_max    = appconfig.getMaxLengthOuput(),
            seed          = appconfig.getSeed(),
            indentsymb    = appconfig.getIndentCharacter(),
            censorsymb    = appconfig.getCensorSymbol(),
            mainfct       = FUNCTION_NAME_MAIN,
        )
    );
    lines.append('');
    lines += documents.generateCode(offset=0, preambles=preambles, globalvars=globalvars);
    lines.append('');
    lines += formatTextBlockAsList(
        _lines_post.format()
    );
    writeTextFile(appconfig.getFileTranspiled(rel=False), lines);
    return;

def displayTreeBranch(
    path:       str,
    anon:       bool = False,
    prefix:     str  = '',
    indentsymb: str  = '    ',
    branchsymb: str  = '  |____',
    depth:      int  = 0
) -> str:
    return '{prefix}{tab}{branchsymb}`{path}`'.format(
        prefix = prefix,
        tab = indentsymb*(depth if depth == 0 else depth - 1),
        branchsymb = '' if depth == 0 else branchsymb,
        path = appconfig.getCensorSymbol() if anon else path,
    );
