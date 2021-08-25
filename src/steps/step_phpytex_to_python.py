#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys;
import os;
import re;
import random;
from tempfile import NamedTemporaryFile;
from typing import Any;
from typing import Dict;
from typing import Tuple;
from typing import List;

from src.core.log import logInfo;
from src.core.log import getQuietMode;
from src.core.utils import formatTextBlockAsList;
from src.core.utils import writeTextFile;
from src.setup import appconfig;
from src.setup.methods import extractfilename, getTemplatePhpytexLines;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step transpile phpytex to python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step(
    root:           str,
    seed:           int,
    output:         str  = 'main.tex',
    export_params:  str  = '',
    insert_bib:     bool = False,
    comments:       str  = 'auto',
    show_structure: bool = True,
    max_length:     int  = 10000,
    compile_latex:  bool = False,
    **_
) -> List[str]:
    appconfig.setSeed(seed);
    appconfig.setMaxLength(max_length);
    appconfig.setInsertBib(insert_bib);
    appconfig.setIncludes([]);
    appconfig.setDocumentStructure([]);

    # must initialise arrays!
    appconfig.initIndentation(pattern=appconfig.getIndentCharacterRe());
    _main_file = root;
    _output_file = output;
    if isinstance(export_params, str) and not (export_params == ''):
        assert re.match(r'^(\S+\.)*\S+$', export_params), '\033[1mexport-params\033[0m option must by a python-like import path (relative to the root of the project).';
        _param_file = re.sub(r'\.', '/', export_params)
        _param_file, _, _  = extractfilename(path=_param_file, relative=True);
        appconfig.setExportParams(True);
        appconfig.setParamPyImport(export_params);
        appconfig.setParamFile(_param_file);

    _main_file, _, _  = extractfilename(path=_main_file, relative=True);
    _output_file, _, _ = extractfilename(path=_output_file, relative=True, ext='');
    assert not (_main_file == _output_file), 'The output and root files must be different!';
    _stamp_file = appconfig.getStampFile();
    _stamp_file, _, _ = extractfilename(path=_stamp_file, relative=True);
    appconfig.setStampFile(_stamp_file);

    random.seed(seed); # <-- only do this once!
    lines = [];
    _precompile_lines = [];
    _list_of_imports = [];
    _global_vars = [];

    params = {
        'comments': comments,
        'no-comm': (comments is False),
        'no-comm-auto': (comments == 'auto'),
        'show-structure': show_structure,
    };
    Knit(
        filecontents = lines,
        imports      = _list_of_imports,
        verbatim     = _precompile_lines,
        mute         = False,
        silent       = getQuietMode(),
        filename     = dict(
            src      = _main_file,
            main     = '{}.tex'.format(_output_file),
        ),
        params       = params,
    );
    addpreamble(lines=lines, params=params, silent=getQuietMode());
    if appconfig.getExportParams():
        fname_params, _, _ = extractfilename(path=appconfig.getParamFile(), relative=True, ext='py');
        exportParameters(fname=fname_params, globalvars=_global_vars);

    fnameLatex, _, _ = extractfilename(path=appconfig.getLatexFile(), relative=False, ext='tex');
    fnamePy = createmetacode(lines=lines, imports=appconfig.getListOfImports(), globalvars=_global_vars, fname=fnameLatex, compile_latex=compile_latex);

    appconfig.setScriptFile(fnamePy);
    appconfig.setPrecompileLines(_precompile_lines);
    appconfig.setListOfImports(_list_of_imports);

    logInfo('Transpilation (phpytex -> python) complete.');
    return lines;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def addpreamble(lines: List[str], params: Dict[str, Any], silent: bool):
    preamble = [];
    verbatim = [];
    struct = appconfig.getDocumentStructure()[:]
    if isinstance(appconfig.getStampFile(), str) and not(appconfig.getStampFile() == ''):
        appconfig.setDocumentStructure([]);
        Knit(
            filecontents = preamble,
            verbatim     = verbatim,
            mute         = True,
            filename     = dict(
                src      =  appconfig.getStampFile(),
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

def createmetacode(
    fname: str,
    lines: List[str],
    imports: List[str],
    globalvars: List[str],
    compile_latex: bool
) -> str:
    fname_rel, _, _ = extractfilename(path=fname, relative=True, ext='');
    _phpytex_lines = getTemplatePhpytexLines()
    lines_pre = formatTextBlockAsList(
        _phpytex_lines[0].format(
            import_params = '\nimport {} as {};\n'.format(appconfig.getParamPyImport(), appconfig.getParamModuleName()) if appconfig.getExportParams() else '',
            indentchar    = appconfig.getIndentCharacterRe(),
            fname         = fname,
            fname_rel     = fname_rel,
            maxlength     = appconfig.getMaxLength(),
            insertbib     = appconfig.getInsertBib(),
            compilelatex  = compile_latex,
            rootdir       = appconfig.getRootDir(),
            seed          = appconfig.getSeed(),
            imports       = (imports if len(imports) > 0 else ['# no imports']),
            globalvars    = (globalvars if len(globalvars) > 0 else ['    # no global vars']),
        )
    );
    appconfig.setLenPrecode(len(lines_pre));
    lines[:] = lines_pre + lines + formatTextBlockAsList(_phpytex_lines[1].format());
    ## create temp file and write to this:
    fp = NamedTemporaryFile(dir=os.getcwd(), prefix='tmp_', suffix='.py', delete=False);
    fnamePy = fp.name;
    fp.close();
    writeTextFile(fnamePy, lines);
    return fnamePy;
