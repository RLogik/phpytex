#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
import random;
from typing import Any;
from typing import Dict;
from typing import Tuple;
from typing import List;

from src.core.log import logInfo;
from src.core.log import getQuietMode;
from src.core.utils import createNewFileName;
from src.core.utils import formatTextBlockAsList;
from src.core.utils import writeTextFile;
from src.setup import appconfig;
from src.setup.methods import extractPath;
from src.setup.methods import getTemplatePhpytexLines;

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

    # must initialise arrays!
    appconfig.initIndentation(pattern=appconfig.getIndentCharacterRe());

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

    Knit(
        filecontents = lines,
        imports      = _list_of_imports,
        verbatim     = _precompile_lines,
        mute         = False,
        silent       = getQuietMode(),
        filename     = dict(
            src      = appconfig.getFilePhpytex(),
            main     = appconfig.getFileLatex(),
        ),
        params       = params,
    );

    addpreamble(lines=lines, params=params, silent=getQuietMode());

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

def addpreamble(lines: List[str], params: Dict[str, Any], silent: bool):
    preamble = [];
    verbatim = [];
    struct = appconfig.getDocumentStructure()[:]
    if isinstance(appconfig.getFileStamp(), str) and not(appconfig.getFileStamp() == ''):
        appconfig.setDocumentStructure([]);
        Knit(
            filecontents = preamble,
            verbatim     = verbatim,
            mute         = True,
            filename     = dict(
                src      =  appconfig.getFileStamp(),
                main     =  'main',
            ),
            params       = params | { 'no-comm': False, 'no-comm-auto': True },
            dateityp     = 'head'
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

    lines[:] = preamble + lines;
    appconfig.setPrecompileLines(verbatim + appconfig.getPrecompileLines());
    return;

def exportParameters(fname: str, globalvars: List[str]):
    lines = [];
    for key, value in appconfig.getExportVars().items():
        value = "r'" + value + "'" if isinstance(value, str) else str(value);
        # value = "r'" + value + "'" if isinstance(value, str) else json.dumps(value);
        lines.append('{name} = {val};'.format(name=key, val=value));
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
    filecontents: List[str],
    imports:      List[str]                  = [],
    verbatim:     List[Tuple[int, Any, str]] = [],
    filename:     Dict[str, str]             = dict(),
    anon:         bool                       = False,
    mute:         bool                       = False,
    silent:       bool                       = False,
    indent:       Dict[str, int]             = dict(tex=0, struct=0),
    params:       Dict[str, Any]             = {},
    dateityp:     str                        = 'tex',
    chain:        List[str]                  = []
):
    # TODO
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
