#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys;
import os;

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)));

from src.core.path import setAppPath;
from src.core.log import setQuietMode;
from src.core.utils import getCliArgs;
from src.endpoints.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN PROCESS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def enter(*tokens: str, file: str = '', **kwargs: str):
    setQuietMode(('q' in tokens));
    if ('version' in tokens) or ('v' in tokens):
        endpoint_display_version()
    elif ('help' in tokens) or ('info' in tokens) or ('man' in tokens):
        endpoint_display_help()
    else:
        endpoint_run_phpytex(fname=file);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 4;
    path = os.path.dirname(os.path.dirname(__file__));
    setAppPath(path);
    tokens, kwargs = getCliArgs(*sys.argv[1:]);
    enter(*tokens, **kwargs);
