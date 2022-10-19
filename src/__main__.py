#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# NOTE: This file is needed in addition to main.py
#       for the creation of an artefact.
#       It is stored one level higher than src.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)));

from src.setup import *;
from src.core.utils import *;
from src.main import enter;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 0;
    open_source(False);
    tokens, kwargs = getCliArgs(*sys.argv[1:]);
    enter(*tokens, **{
        'file':     '',
        'pathApp':  os.path.dirname(os.path.abspath(__file__)),
        'pathRoot': os.getcwd(),
        **kwargs
    });
