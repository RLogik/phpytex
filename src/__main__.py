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

from src.core.utils import getCliArgs;
from src.setup.methods import setOpenSource;
from src.main import enter;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 0;
    setOpenSource(False);
    tokens, kwargs = getCliArgs(*sys.argv[1:]);
    kwargs = { **dict(
        file     = '',
        pathApp  = os.path.dirname(__file__),
        pathRoot = os.getcwd(),
    ), **kwargs };
    enter(*tokens, **kwargs);
