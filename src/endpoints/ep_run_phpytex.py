#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;

from src.setup import *;
from src.core.log import *;
from src.core.utils import *;
from src.steps.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENDPOINT run phpytex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def endpoint(fnameConfig: str, parameters: dict, **_):
    log_plain(dedent('''
        ----------------------
        |     \033[32;1m(PH(p)y)tex\033[0m    |
        ----------------------
    '''));
    step_configure(fnameConfig=fnameConfig, extra_parameters=parameters);
    if appconfig.getOptionIgnore():
        log_info('\033[32;1m(PH(p)y)tex\033[0m transpilation will be skipped.');
        return;
    step_create();
    step_transpile();
    if appconfig.getOptionDebug():
        log_info('The result of transpilation can be viewed in \033[1m{fnamePy}\033[0m'.format(fnamePy=appconfig.getFileTranspiled()));
        return;
    step_compile();
    return;
