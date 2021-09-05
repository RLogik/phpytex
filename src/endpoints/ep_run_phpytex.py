#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.setup import appconfig;
from src.core.log import *;
from src.core.utils import formatTextBlock;
from src.core.utils import getAttribute;
from src.core.utils import toPythonKeysDict;
from src.steps.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENDPOINT run phpytex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def endpoint(fname: str, **_):
    step_readconfig(fname=fname);
    if appconfig.getOptionIgnore():
        logInfo('\033[32;1m(PH(p)y)tex\033[0m transpilation will be skipped.');
        return;
    logPlain(formatTextBlock('''
        ----------------------
        |     \033[32;1m(PH(p)y)tex\033[0m    |
        ----------------------
    '''));
    step_create();
    lines = [];
    step_phpytex_to_python(lines=lines);
    if appconfig.getOptionDebug():
        logInfo('See output file: \033[1m{fnamePy}\033[0m'.format(fnamePy=appconfig.getFileScript()));
        return;
    step_python_to_latex(lines=lines);
    if appconfig.getOptionCompileLatex():
        step_latex_to_pdf();
    return;
