#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.setup import appconfig;
from src.core.log import *;
from src.core.utils import formatTextBlock;
from src.steps.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENDPOINT run phpytex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def endpoint(fname: str, **_):
    logPlain(formatTextBlock('''
        ----------------------
        |     \033[32;1m(PH(p)y)tex\033[0m    |
        ----------------------
    '''));
    step_configure(fname=fname);
    if appconfig.getOptionIgnore():
        logInfo('\033[32;1m(PH(p)y)tex\033[0m transpilation will be skipped.');
        return;
    step_create();
    step_transpile();
    if appconfig.getOptionDebug():
        logInfo('The result of transpilation can be viewed in \033[1m{fnamePy}\033[0m'.format(fnamePy=appconfig.getFileTranspiled()));
        return;
    step_compile();
    return;
