#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;
import re;
from typing import List;
from typing import Union;

WORKINGDIRECTORY = os.getcwd();
SOURCEDIRECTORY = os.path.dirname(os.path.realpath(__file__));

from .core.config import Struct;
from .core.logger import Logger;
from .core.utils import parse_cli_args;
from .info.versions import get_version;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

log: Logger;
VERSION: Union[str, None] = None;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    global VERSION;
    tokens, kwargs = parse_cli_args(sys.argv[1:]);
    setup_log();
    try:
        VERSION = get_version(SOURCEDIRECTORY);
    except Exception as err:
        VERSION = None;
        log.error(str(err));
    log.info('At the moment nothing has been implemented.');
    run_cli_arguments(tokens=tokens, **kwargs);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXLIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setup_log():
    global log;
    fname = os.path.join(SOURCEDIRECTORY, 'config.yml');
    config = Struct.get_from_file(fname);
    config_logging = Struct.get_value(config, 'logging', default=dict());
    log = Logger(config_logging);
    return;

def run_cli_arguments(tokens: List[str], **kwargs):
    global log;
    global VERSION;
    if 'version' in tokens:
        log.info('This is version \033[1;92m{}\033[0m of the \033[1;32m(Ph(P)y)TeX\033[0m programme.'.format(VERSION or '???'));
    elif 'create' in tokens:
        log.info('Methods for \033[1;32m(Ph(P)y)create\033[0m are under construction.');
    elif 'transpile' in tokens:
        log.info('Methods for \033[1;32m(Ph(P)y)TeX\033[0m are under construction.');
    else:
        log.info('Try calling the programme with the arguments \033[1;94m--version\033[0m, \033[1;94m--help\033[0m, \033[1;94m--create\033[0m, \033[1;94m--traanspile\033[0m.');
    return;
