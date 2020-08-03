#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;

from .make import Make;
from .parser import extract_specs;
from .parser import process_specs;
from ...core.logger import Logger;
from ...info.arguments import ArgumentValues;
from ...values.struct import Struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LOG: Logger;
MODULENAME: str = 'create';
CONFIG: Struct;
WORKINGDIRECTORY: str;
MAKE: Make;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(log: Logger, config: Struct, argumentValues: ArgumentValues):
    global LOG;
    global CONFIG;
    global WORKINGDIRECTORY;
    global MAKE;
    global MODULENAME;

    LOG = log;
    CONFIG = config;
    WORKINGDIRECTORY = os.getcwd();
    MAKE = Make(log=LOG, wd=WORKINGDIRECTORY);

    LOG.info(
        '',
        'Starting the \033[1;32m{module}\033[0m subprogramme.'.format(module=MODULENAME),
        ''
    );
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
    for subpath, spec in extract_specs(recursive, CONFIG, WORKINGDIRECTORY):
        process_specs(MAKE, subpath, spec, subpath == WORKINGDIRECTORY);
    return;
