#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.setup import *;
from src.core.log import *;
from src.core.utils import pipeCall;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step transpile python to latex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step():
    log_info('CONVERSION (python -> latex [+ latex -> pdf]) STARTED.');
    fnamePy = appconfig.getFileTranspiled(rel=True);
    fnameLatex = appconfig.getFileOutput(rel=True);
    execTranspiledCode(fnamePy=fnamePy, fnameLatex=fnameLatex);
    log_info('CONVERSION (python -> latex) COMPLETE.');
    if appconfig.getOptionCompileLatex():
        log_info('CONVERSION (latex -> pdf) COMPLETE.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def execTranspiledCode(fnamePy: str, fnameLatex: str):
    try:
        cmd = re.split(r'\s+', appconfig.getPythonPath());
        log_info('CALL < \033[94;1m{}\033[0m >'.format(' '.join(cmd + [fnamePy])));
        pipeCall(*cmd, fnamePy);
        os.remove(fnamePy);
    except:
        log_fatal(
            'An error occurred during (python -> latex -> pdf) conversion.',
            '  - Consult the error logs and the script \033[1m{path}\033[0m for more information.'.format(path=fnamePy),
            '  - Partial output may also be found in \033[1m{path}\033[0m.'.format(path=fnameLatex)
        );
    return;
