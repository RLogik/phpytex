#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys;
import re;
from types import TracebackType;
from typing import List;

from src.core.log import logError;
from src.core.log import logFatal;
from src.core.log import logInfo;
from src.core.log import logPlain;
from src.core.utils import callPython;
from src.core.utils import formatTextBlock;
from src.core.utils import formatTextBlockAsList;
from src.core.utils import write_file;
from src.setup import appconfig;
from src.setup.methods import extractfilename;
from src.setup.methods import getTemplatePhpytexLines;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step transpile python to latex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step(
    lines:          List[str],
    debug:          bool = False,
    compile_latex:  bool = False,
    **_
) -> List[str]:
    globalvars = [];
    hauptfile, _, _ = extractfilename(path=appconfig.getOutputFile(), relative=False, ext='tex');
    if appconfig.getExportParams():
        fname_params, _, _ = extractfilename(path=appconfig.getParamFile(), relative=True, ext='py');
        exportParameters(fname=fname_params, globalvars=globalvars);
    createmetacode(lines=lines, imports=appconfig.getListOfImports(), globalvars=globalvars, fname=hauptfile, compile_latex=compile_latex);
    execmetacode(lines=lines, fname=hauptfile, debug=debug);
    logInfo('Transpilation (python -> latex) complete.');
    return lines;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def createmetacode(fname: str, lines: List[str], imports: List[str], globalvars: List[str], compile_latex: bool):
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
    return;

def execmetacode(lines: List[str], fname: str, debug: bool):
    global ERROR;
    global PYERROR;

    fname_rel, _, _ = extractfilename(path=fname, relative=True, ext='');
    write_file(fname, lines);
    if debug:
        logInfo('See output file: \033[1m{fname}.tex\033[0m'.format(fname=fname_rel));
        return;
    try:
        callPython(fnameScript=fname_rel+'.tex');
    except:
        ERROR = True;
        PYERROR = True;
        _, err, tb = sys.exc_info();

        try:
            n = tb.tb_lineno - 1 if isinstance(tb, TracebackType) else 0;
            line_err = lines[n];
            n -= appconfig.getLenPrecode();
            linenr = -1; ## globale Zeilennummer
            precompilelines = [];
            __LINENR__ = -1;
            __FNAME__ = '???';
            for k, ignore, line in appconfig.getPrecompileLines():
                if ignore is True:
                    m = re.match(r'^\s*__FNAME__\s*=\s*[\'\"](.*)[\'\"](?:;|)\s*$', line);
                    if m:
                        __FNAME__ = m.group(1);
                    linenr += 1;
                elif ignore is False:
                    linenr += 1;
                precompilelines.append((linenr, ignore, line));
                if linenr >= n:
                    __LINENR__ = int(k); ## lokale Zeilennummer innerhalb Datei
                    break;
                continue;

            logError(formatTextBlock(
                '''
                -----------------------------------------------------------------
                !!! (PH(p)y)TeX compilation failed !!!
                  FILE: {fname}
                  LINE: {lineno} (local position in file).
                !!! Syntax error !!!
                -----------------------------------------------------------------
                {err}
                -----------------------------------------------------------------
                (siehe Outputdatei)
                '''.format(
                    fname  = __FNAME__,
                    lineno = __LINENR__ + 1,
                    err    = line_err
                ))
            );

            ## print to main tex file:
            with open(fname, 'w+') as fp:
                logPlain(*[line for k, ignore, line in precompilelines if k < n and not (ignore is True)], file=fp);
                logPlain(
                    r'''
                    -----------------------------------------------------------------
                    !!! (PH(p)y)TeX compilation failed !!!
                      FILE: {fname}
                      LINE: {lineno} (local position in file).
                    !!! Syntax error !!!
                    -----------------------------------------------------------------
                    '''.format(
                        fname  = __FNAME__,
                        lineno = __LINENR__ + 1,
                    ),
                    file=fp
                );
                logPlain('', *[line for k, ignore, line in precompilelines if k == n and ignore is False], file=fp);
                logPlain(r'''-----------------------------------------------------------------''', file=fp);
        except:
            logFatal(err);
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
    write_file(fname, lines, force_create_path=True);
    return;
