#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;

from .make import CompilerConfig;
from .make import Make;
from .parser import extract_specs;
from .parser import process_specs;
from ...core.logger import LoggerService;
from ...info.arguments import ArgumentValues;
from ...info.information import InformationService;
from ...values.struct import Struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INFO: InformationService;
LOG: LoggerService;
MODULENAME: str = 'create';
CONFIG: Struct;
WORKINGDIRECTORY: str;
MAKE: Make;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(info: InformationService, log: LoggerService, config: Struct, argumentValues: ArgumentValues):
    global INFO;
    global LOG;
    global CONFIG;
    global WORKINGDIRECTORY;
    global MAKE;
    global MODULENAME;

    INFO = info;
    LOG = log;
    CONFIG = config;
    WORKINGDIRECTORY = os.getcwd();
    MAKE = Make(log=LOG, wd=WORKINGDIRECTORY);

    LOG.info(
        '',
        'Starting the \033[1;32m{module}\033[0m subprogramme.'.format(module=MODULENAME),
    );
    INFO.console_print_used_arguments(argumentValues);
    extract_and_process_specs(recursive=argumentValues.getValueAsBoolean('recursive'));
    LOG.info(
        '',
        'The \033[1;32m{module}\033[0m subprogramme has ended.'.format(module=MODULENAME),
        ''
    );
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def extract_and_process_specs(recursive: bool):
    global LOG;
    global INFO;

    arguments = INFO.parse_arguments('transpile');
    basiccommand = INFO.get_attributes('programmes', 'transpile', 'command');
    compilerConfig = CompilerConfig(arguments);
    for subpath, spec in extract_specs(recursive, CONFIG, WORKINGDIRECTORY):
        LOG.info('');
        process_specs(MAKE, basiccommand, compilerConfig, subpath, spec, subpath == WORKINGDIRECTORY);
    return;
