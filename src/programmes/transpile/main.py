#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;

from ...core.logger import LoggerService;
from ...info.arguments import ArgumentValues;
from ...info.information import InformationService;
from ...values.struct import Struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INFO: InformationService;
LOG: LoggerService;
MODULENAME: str = 'transpile';
CONFIG: Struct;
WORKINGDIRECTORY: str;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(info: InformationService, log: LoggerService, config: Struct, argumentValues: ArgumentValues):
    global INFO;
    global LOG;
    global CONFIG;
    global WORKINGDIRECTORY;
    global MODULENAME;

    INFO = info;
    LOG = log;
    CONFIG = config;
    WORKINGDIRECTORY = os.getcwd();

    LOG.info(
        '',
        'Starting the \033[1;32m{module}\033[0m subprogramme.'.format(module=MODULENAME),
    );
    INFO.console_print_used_arguments(argumentValues);
    LOG.info(
        '',
        'The \033[1;32m{module}\033[0m subprogramme has ended.'.format(module=MODULENAME),
        ''
    );
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
