#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.maths import *;
from src.local.typing import *;

from src.core.log import *;
from src.core.utils import createNewFileName;
from src.core.utils import formatTextBlockAsList;
from src.core.utils import readTextFile;
from src.core.utils import unique;
from src.core.utils import writeTextFile;
from src.customtypes.exports import *;
from src.setup import appconfig;
from src.setup.methods import extractPath;
from src.setup.methods import getTemplatePhpytexLines;
from src.parsers.phpytex import parseText;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step transpile phpytex to python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step(lines: List[str]):
    appconfig.setIncludes([]);
    appconfig.setDocumentStructure([]);
    random.seed(appconfig.getSeed()); # <-- only do this once!
    lines[:] = [];
    root = appconfig.getPathRoot();
    indentsymb = appconfig.getIndentCharacter();
    preamble = [];

    params = {
        'no-comm':       (appconfig.getOptionComments() is False),
        'no-comm-auto':  (appconfig.getOptionComments() == 'auto'),
    };

    ## Initialise structures for recording transpilation units:
    documents = TranspileDocuments(root = root, indentsymb = indentsymb);
    imports = TranspileBlocks();

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
    fnameLatex, _, _ = extractPath(path=appconfig.getFileLatex(), relative=False, ext='tex');
    fnamePy = createNewFileName(dir=root, nameinit='phpytex_main.py', namescheme='phpytex_main_{}.py');
    createmetacode(
        lines      = lines,
        documents  = documents,
        imports    = imports,
        preamble   = preamble,
        globalvars = globalvars,
        fname      = fnameLatex,
        fnameOut   = fnamePy
    );

    appconfig.setFileScript(fnamePy);
    # appconfig.setPrecompileLines(_precompile_lines);
    # appconfig.setListOfImports(_list_of_imports);

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
    lines:      List[str],
    documents:  TranspileDocuments,
    imports:    TranspileBlocks,
    fname:      str,
    fnameOut:   str,
    preamble:   List[str],
    globalvars: List[str]
):
    lines[:] = documents.generateCode(offset=0, preamble=preamble, globalvars=globalvars);
    fname_rel, _, _ = extractPath(path=fname, relative=True, ext='');
    _phpytex_lines = getTemplatePhpytexLines()
    lines_pre = formatTextBlockAsList(
        _phpytex_lines.format(
            indentchar    = appconfig.getIndentCharacterRe(),
            fname         = fname,
            fname_rel     = fname_rel,
            maxlength     = appconfig.getMaxLengthOuput(),
            insertbib     = appconfig.getOptionInsertBib(),
            rootdir       = appconfig.getPathRoot(),
            seed          = appconfig.getSeed(),
            imports       = '\n'.join(imports.generateCode(offset=0)),
        )
    );
    appconfig.setLenPrecode(len(lines_pre));
    lines[:] = lines_pre + lines;
    ## create temp file and write to this:
    writeTextFile(fnameOut, lines);
    return;
