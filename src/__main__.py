#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;
from typing import List;

WORKINGDIRECTORY = os.getcwd();
SOURCEDIRECTORY = os.path.dirname(os.path.realpath(__file__));

from .core.config import extractConfig;
from .core.logger import Logger;
from .core.utils import parse_cli_args;
from .core.utils import get_dict_value;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

log: Logger;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    tokens, kwargs = parse_cli_args(sys.argv[1:]);
    setup_log();
    log.info('This is the \033[1;32m(Ph(P)y)TeX\033[0m! programme. At the moment nothing has been implemented.');
    run_command(tokens=tokens, **kwargs);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXLIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setup_log():
    global log;
    config = extractConfig(os.path.join(SOURCEDIRECTORY, 'config.yml'));
    config_logging = get_dict_value(config, 'logging', default=dict());
    log = Logger(config_logging);
    return;

def run_command(tokens: List[str], **kwargs):
    global log;
    log.info('You called this programme with the tokens:   ' + str(tokens) + '.');
    log.info('You called this programme with the keywords: ' + str(kwargs) + '.');
    return;
