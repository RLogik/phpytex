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
    _precompile_lines = [];
    _list_of_imports = [];
    _global_vars = [];

    params = {
        'comments': appconfig.getOptionComments(),
        'no-comm': (appconfig.getOptionComments() is False),
        'no-comm-auto': (appconfig.getOptionComments() == 'auto'),
        'show-structure': appconfig.getOptionShowStructure(),
    };

    _documents = TranspileDocuments(root=appconfig.getPathRoot(), indentsymb=appconfig.getIndentCharacter());

    Knit(
        path      = appconfig.getFilePhpytex(),
        documents = _documents,
        imports   = _list_of_imports,
        verbatim  = _precompile_lines,
        mute      = False,
        silent    = getQuietMode(),
        params    = params
    );

    addPreamble(
        path      = appconfig.getFileStamp(),
        documents = _documents,
        silent    = getQuietMode(),
        params    = params
    );

    if appconfig.getExportParams():
        fname_params, _, _ = extractPath(path=appconfig.getFileParamsPy(), relative=True, ext='py');
        exportParameters(fname=fname_params, globalvars=_global_vars);

    fnameLatex, _, _ = extractPath(path=appconfig.getFileLatex(), relative=False, ext='tex');
    fnamePy = createNewFileName(dir=appconfig.getPathRoot(), nameinit='phpytex_main.py', namescheme='phpytex_main_{}.py');
    createmetacode(lines=lines, imports=_list_of_imports, globalvars=_global_vars, fname=fnameLatex, fnameOut=fnamePy);

    appconfig.setFileScript(fnamePy);
    appconfig.setPrecompileLines(_precompile_lines);
    appconfig.setListOfImports(_list_of_imports);

    logInfo('Transpilation (phpytex -> python) complete.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def addPreamble(
    path: str,
    documents: TranspileDocuments,
    params: Dict[str, Any],
    silent: bool
):
    preamble = [];
    verbatim = [];
    struct = appconfig.getDocumentStructure()[:]
    if isinstance(path, str) and not(path == ''):
        appconfig.setDocumentStructure([]);
        Knit(
            # filecontents = preamble,
            path      = path,
            documents = documents,
            verbatim  = verbatim,
            mute      = True,
            params    = params | { 'no-comm': False, 'no-comm-auto': True }
        );
        appconfig.setDocumentStructure(struct[:]);

    # if not silent:
    #     addpytexline(lines=preamble, verbatim=verbatim, expr=[
    #         '%% ********************************************************************************',
    #         '%% DOCUMENT STRUCTURE:',
    #         '%% ~~~~~~~~~~~~~~~~~~~',
    #         '%%',
    #     ] + struct + [
    #         '%%',
    #         '%% DOCUMENT-RANDOM-SEED: '+str(appconfig.getSeed()),
    #         '%% ********************************************************************************',
    #     ], anon=False, mode='meta');

    # lines[:] = preamble + lines;
    appconfig.setPrecompileLines(verbatim + appconfig.getPrecompileLines());
    return;

def exportParameters(fname: str, globalvars: List[str]):
    lines = [];
    for key, (value, codedvalue) in appconfig.getExportVars().items():
        lines.append('{name} = {val};'.format(name=key, val=codedvalue));
        # globalvars.append('{indent}from {importpath} import {name};'.format(
        #     indent     = appconfig.getIndentCharacter()*1,
        #     importpath = appconfig.getParamPyImport(),
        #     name       = key,
        # ));
        globalvars.append('{indent}{name} = {mod}.{name};'.format(
            indent = appconfig.getIndentCharacter()*1,
            name   = key,
            mod    = appconfig.getParamModuleName(),
        ));
    if len(lines) > 0:
        lines = ['#!/usr/bin/env python3', '# -*- coding: utf-8 -*-', ''] + lines;
    else:
        lines = ['#!/usr/bin/env python3', '# -*- coding: utf-8 -*-'];
    writeTextFile(path=fname, lines=lines, force_create_path=True);
    return;

def Knit(
    path:         str,
    documents:    TranspileDocuments,
    imports:      List[str]                  = [],
    verbatim:     List[Tuple[int, Any, str]] = [],
    anon:         bool                       = False,
    mute:         bool                       = False,
    silent:       bool                       = False,
    params:       Dict[str, Any]             = {},
    chain:        List[str]                  = [],
    ishead:       bool                       = True
):
    lines = readTextFile(path);
    indentation = IndentationTracker(
        symb       = appconfig.getIndentCharacter(),
        pattern    = appconfig.getIndentCharacterRe(),
        is_legacy  = appconfig.getOptionLegacy(),
    );
    blocks = parseText(lines, indentation);
    documents.addDocument(path=path);
    documents.addBlocks(path=path, blocks=blocks);
    for line in documents.generateCode():
        logDebug(line);
    return;

def createmetacode(
    fname: str,
    fnameOut: str,
    lines: List[str],
    imports: List[str],
    globalvars: List[str]
):
    fname_rel, _, _ = extractPath(path=fname, relative=True, ext='');
    _phpytex_lines = getTemplatePhpytexLines()
    lines_pre = formatTextBlockAsList(
        _phpytex_lines.format(
            import_params = '\nimport {} as {};\n'.format(appconfig.getImportParamsPy(), appconfig.getParamModuleName()) if appconfig.getExportParams() else '',
            indentchar    = appconfig.getIndentCharacterRe(),
            fname         = fname,
            fname_rel     = fname_rel,
            maxlength     = appconfig.getMaxLengthOuput(),
            insertbib     = appconfig.getOptionInsertBib(),
            rootdir       = appconfig.getPathRoot(),
            seed          = appconfig.getSeed(),
            imports       = '\n    '.join(imports if len(imports) > 0 else [ '# no imports' ]),
            globalvars    = '\n    '.join(globalvars if len(globalvars) > 0 else [ '# no global vars' ]),
        )
    );
    appconfig.setLenPrecode(len(lines_pre));
    lines[:] = lines_pre + lines;
    ## create temp file and write to this:
    writeTextFile(fnameOut, lines);
    return;
