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
    fnamePy = appconfig.getFileTranspiled(rel=True);
    fnameLatex = appconfig.getFileOutput(rel=True);
    execTranspiledCode(fnamePy=fnamePy, fnameLatex=fnameLatex);
    logInfo('CONVERSION (python -> latex) COMPLETE.');
    if appconfig.getOptionCompileLatex():
        logInfo('CONVERSION (latex -> pdf) COMPLETE.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def execTranspiledCode(fnamePy: str, fnameLatex: str):
    try:
        cmd = re.split(r'\s+', appconfig.getPythonPath());
        logInfo('CALL < \033[94;1m{}\033[0m >'.format(' '.join(cmd + [fnamePy])));
        pipeCall(*cmd, fnamePy);
        os.remove(fnamePy);
    except:
        logFatal(
            'An error occurred during (python -> latex -> pdf) conversion.',
            '  - Consult the error logs and the script \033[1m{path}\033[0m for more information.'.format(path=fnamePy),
            '  - Partial output may also be found in \033[1m{path}\033[0m.'.format(path=fnameLatex)
        );
    return;
