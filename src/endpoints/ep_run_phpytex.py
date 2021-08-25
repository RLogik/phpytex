#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.setup import appconfig
from src.core.log import logInfo;
from src.core.log import logPlain;
from src.core.utils import formatTextBlock;
from src.core.utils import getAttribute;
from src.core.utils import toPythonKeysDict;
from src.steps.exports import *;
from src.parsers.phpytex import setIndentation;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENDPOINT run phpytex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def endpoint(
    fname: str,
    **_
):
    logPlain(formatTextBlock('''
        ----------------------
        |     \033[32;1m(PH(p)y)tex\033[0m    |
        ----------------------
    '''));
    config = step_readconfig(fname=fname);
    option_ignore = getAttribute(config, 'ignore', expectedtype=bool, default=False);
    if option_ignore:
        logInfo('(PH(p)y)tex Transpilation will be skipped.');
        return;
    config_compile = getAttribute(config, 'compile', 'options', expectedtype=dict, default=None) \
                        or getAttribute(config, 'compile', expectedtype=dict, default={});
    option_debug = getAttribute(config_compile, 'debug', expectedtype=bool, default=False);
    setIndentation(**config_compile);
    step_create(**config);
    lines = step_phpytex_to_python(**toPythonKeysDict(config_compile));
    if option_debug:
        logInfo('See output file: \033[1m{fnamePy}\033[0m'.format(fnamePy=appconfig.getScriptFile()));
    else:
        step_python_to_latex(lines=lines, **toPythonKeysDict(config_compile));
        step_latex_to_pdf();
    return;
