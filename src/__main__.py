#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;
import re;
from typing import List;
from typing import Union;

from .core.config import Struct;
from .core.logger import Logger;
from .core.utils import parse_cli_args;
from .info.info import get_version;
from .programmes import phpycreate;
from .programmes import phpytex;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WORKINGDIRECTORY = os.getcwd();
LOG: Logger;
VERSION: Union[str, None] = None;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    args = sys.argv[1:];
    tokens, _ = parse_cli_args(args);
    setup_log();
    determine_version();
    run_cli_arguments(args, tokens);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXLIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setup_log():
    global LOG;

    config = Struct.get_from_file('config.yml');
    config_logging = Struct.get_value(config, 'logging', default=dict());
    LOG = Logger(config_logging);
    return;

def determine_version():
    global LOG;
    global VERSION;

    try:
        VERSION = get_version();
    except Exception as err:
        VERSION = None;
        LOG.error(str(err));
    return;

def run_cli_arguments(args: List[str], tokens: List[str]):
    global LOG;
    global VERSION;

    if 'create' in tokens:
        phpycreate.main(LOG, VERSION or '???', *args);
    elif 'transpile' in tokens:
        phpytex.main(LOG, VERSION or '???', *args);
    elif 'version' in tokens:
        LOG.plain(VERSION or '???');
    elif 'help' in tokens:
        LOG.info('Try calling \033[1;96mphpytex --transpile --help\033[0m, \033[1;96mphpytex --create --help\033[0m.');
    else:
        LOG.info('Try calling \033[1;96mphpytex\033[0m [\033[1;96m--version\033[0m|\033[1;96m--help\033[0m].');
    return;
