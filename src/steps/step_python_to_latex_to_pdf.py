#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.misc import *;
from src.local.system import *;
from src.local.typing import *;

from src.core.log import *;
from src.core.utils import pipeCall;
from src.setup import appconfig;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step transpile python to latex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step():
    logInfo('CONVERSION (python -> latex [+ latex -> pdf]) STARTED.');
    fnamePy = appconfig.getFileScript();
    fnameLatex = appconfig.getFileLatex();
    execmetacode(fnamePy=fnamePy, fnameLatex=fnameLatex);
    logInfo('CONVERSION (python -> latex) COMPLETE.');
    if appconfig.getOptionCompileLatex():
        logInfo('CONVERSION (latex -> pdf) COMPLETE.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def execmetacode(fnamePy: str, fnameLatex: str):
    try:
        cmd = re.split(r'\s+', appconfig.getPythonPath());
        pipeCall(*cmd, fnamePy);
        os.remove(fnamePy);
    except:
        appconfig.setHasError(True);
        appconfig.setHasPyError(True);
        _, err, tb = sys.exc_info();
        # ## ERSETZUNG VON \bibliography-Befehlen durch Inhalte + Anonymisierung:
        # try:
        # except Exception as e:
        #     ## Provide information, then exit with status 1.
        #     print("-----------------------------------------------------------------");
        #     print("!!! (PH(p)y)TeX Compile error !!!");
        #     if ____error_eval____:
        #         ____last_latex____ = eval("'"+____last_latex____+"'");
        #         print("  FILE: "+str(__FNAME__));
        #         print("  LINE: "+str(__LINENR__ + 1)+" (local position in file).");
        #         print("!!! Line could not be evaluated !!!");
        #         print("-----------------------------------------------------------------");
        #         print(____last_latex____);
        #         print("-----------------------------------------------------------------");
        #         ____forceprint("-----------------------------------------------------------------");
        #         ____forceprint("!!! (PH(p)y)TeX Compile error !!!");
        #         ____forceprint("  FILE: "+str(__FNAME__));
        #         ____forceprint("  LINE: "+str(__LINENR__ + 1)+" (local position in file).");
        #         ____forceprint("!!! Line could not be evaluated !!!");
        #         ____forceprint("-----------------------------------------------------------------");
        #         ____forceprint(____last_latex____);
        #         ____forceprint("-----------------------------------------------------------------");
        #     else:
        #         print("-----------------------------------------------------------------");
        #         # print(sys.exc_info());
        #         print(e);
        #         print("-----------------------------------------------------------------");
        #     exit(1);
        #
        # try:
        #     n = tb.tb_lineno - 1 if isinstance(tb, TracebackType) else 0;
        #     line_err = lines[n];
        #     n -= appconfig.getLenPrecode();
        #     linenr = -1; ## globale Zeilennummer
        #     precompilelines = [];
        #     __LINENR__ = -1;
        #     __FNAME__ = '???';
        #     for k, ignore, line in appconfig.getPrecompileLines():
        #         if ignore is True:
        #             m = re.match(r'^\s*__FNAME__\s*=\s*[\'\"](.*)[\'\"](?:;|)\s*$', line);
        #             if m:
        #                 __FNAME__ = m.group(1);
        #             linenr += 1;
        #         elif ignore is False:
        #             linenr += 1;
        #         precompilelines.append((linenr, ignore, line));
        #         if linenr >= n:
        #             __LINENR__ = int(k); ## lokale Zeilennummer innerhalb Datei
        #             break;
        #         continue;
        #
        #     logError(formatTextBlock(
        #         '''
        #         -----------------------------------------------------------------
        #         !!! (PH(p)y)TeX compilation failed !!!
        #           FILE: {fname}
        #           LINE: {lineno} (local position in file).
        #         !!! Syntax error !!!
        #         -----------------------------------------------------------------
        #         {err}
        #         -----------------------------------------------------------------
        #         (siehe Outputdatei)
        #         '''.format(
        #             fname  = __FNAME__,
        #             lineno = __LINENR__ + 1,
        #             err    = line_err
        #         ))
        #     );
        #
        #     ## print to main tex file:
        #     with open(fnameLatex, 'w+') as fp:
        #         logPlain(*[line for k, ignore, line in precompilelines if k < n and not (ignore is True)], file=fp);
        #         logPlain(
        #             r'''
        #             -----------------------------------------------------------------
        #             !!! (PH(p)y)TeX compilation failed !!!
        #               FILE: {fname}
        #               LINE: {lineno} (local position in file).
        #             !!! Syntax error !!!
        #             -----------------------------------------------------------------
        #             '''.format(
        #                 fname  = __FNAME__,
        #                 lineno = __LINENR__ + 1,
        #             ),
        #             file=fp
        #         );
        #         logPlain('', *[line for k, ignore, line in precompilelines if k == n and ignore is False], file=fp);
        #         logPlain(r'''-----------------------------------------------------------------''', file=fp);
        # except:
        #     os.remove(fnamePy);
        #     logFatal(err);
        logFatal('An error occurred during either (python -> latex -> pdf) conversion.');
    return;
