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

import sys;
import os;

sys.path.insert(0, os.path.dirname(__file__));

from src.core.path import setAppPath;
from src.core.utils import getCliArgs;
from src.setup.methods import setOpenSource;
from src.main import enter;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 4;
    setOpenSource(False);
    path = os.path.dirname(__file__);
    setAppPath(path);
    tokens, kwargs = getCliArgs(*sys.argv[1:]);
    enter(*tokens, **kwargs);
