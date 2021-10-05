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
    fnamePy = appconfig.getFileTranspiled();
    fnameLatex = appconfig.getFileOutput();
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
        logFatal('An error occurred during either (python -> latex -> pdf) conversion.');
    return;
