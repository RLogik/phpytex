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
from src.setup.methods import extractPath;
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
    root = appconfig.getPathRoot();
    indentsymb = appconfig.getIndentCharacter();
    params = {
        'no-comm':      (appconfig.getOptionComments() is False),
        'no-comm-auto': (appconfig.getOptionComments() == 'auto'),
    };

    ## Initialise structures for recording transpilation units:
    random.seed(appconfig.getSeed()); # <-- only do this once!
    preamble = [];
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
    preamble.append(name);
    transpileDocument(
        path        = appconfig.getFileStamp(),
        documents   = documents,
        imports     = TranspileBlocks(),
        name        = name,
        is_preamble = True,
        silent      = True,
        params      = params | { 'no-comm': False, 'no-comm-auto': True }
    );

    ## Transpile document file:
    transpileDocument(
        path        = appconfig.getFilePhpytex(),
        documents   = documents,
        imports     = imports,
        name        = '',
        is_preamble = False,
        silent      = getQuietMode(),
        params      = params
    );

    ## Add document structure:
    name = 'tree';
    if appconfig.getOptionShowStructure():
        preamble.append(name);
    blocks = TranspileBlocks([documents.documentTree(seed=appconfig.getSeed())]);
    documents.addPreamble(name=name, blocks=blocks);

    ## Create `parameters.py`:
    createImportFileParameters(
        path      = os.path.join(root, appconfig.getFileParamsPy()),
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
        fname      = appconfig.getFileLatex(),
        fnameOut   = appconfig.getFileScript(),
        documents  = documents,
        imports    = imports,
        preamble   = preamble,
        globalvars = globalvars
    );
    logInfo('Transpilation (phpytex -> python) complete.');
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
    indentation = IndentationTracker(
        symb       = appconfig.getIndentCharacter(),
        pattern    = appconfig.getIndentCharacterRe(),
        is_legacy  = appconfig.getOptionLegacy(),
    );
    if is_preamble:
        blocks = TranspileBlocks();
        for block in parseText(lines, indentation):
            if not re.match(r'^text:comment', block.kind):
                continue;
            blocks.append(block);
        documents.addPreamble(name=name, blocks=blocks);
    else:
        if path in documents.paths:
            return;
        blocks = TranspileBlocks();
        for block in parseText(lines, indentation):
            kind = block.kind;
            if is_preamble:
                if not re.match(r'^text:comment', kind):
                    continue;
            else:
                if kind == 'code:import':
                    imports.append(block);
                    continue;
                if re.match(r'^text:comment', kind):
                    if params['no-comm'] or ( re.match(r'^.*:simple$', kind) and params['no-comm-auto'] ):
                        continue;
            blocks.append(block);
        documents.addDocument(path=path);
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
    fname:      str,
    fnameOut:   str,
    documents:  TranspileDocuments,
    imports:    TranspileBlocks,
    preamble:   List[str],
    globalvars: List[str]
):
    _lines_pre = getTemplatePhpytexLinesPre();
    _lines_post = getTemplatePhpytexLinesPost();
    lines = [];
    lines += formatTextBlockAsList(
        _lines_pre.format(
            imports       = '\n'.join(imports.generateCode()),
            root          = appconfig.getPathRoot(),
            path          = extractPath(path=appconfig.getFileLatex(), relative=False, ext='tex'),
            fname         = extractPath(path=fname, relative=True, ext=''),
            insert_bib    = appconfig.getOptionInsertBib(),
            compile_latex = appconfig.getOptionCompileLatex(),
            length_max    = appconfig.getMaxLengthOuput(),
            seed          = appconfig.getSeed(),
            mainfct       = FUNCTION_NAME_MAIN,
        )
    );
    lines += documents.generateCode(offset=0, preamble=preamble, globalvars=globalvars);
    lines += formatTextBlockAsList(
        _lines_post.format()
    );
    writeTextFile(fnameOut, lines);
    return;
