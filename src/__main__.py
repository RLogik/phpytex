#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;
from typing import List;
from typing import Tuple;
from typing import Union;

from .values.struct import Struct;
from .core.logger import Logger;
from .info.info import Info;
from .programmes.transpile import main as subprogramme_transpile;
from .programmes.create import main as subprogramme_create;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WORKINGDIRECTORY = os.getcwd();
LOG: Logger;
INFO: Info;
VERSION: Union[str, None] = None;
PARTS: List[Tuple[str, str, str, str]];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    args = sys.argv[1:];

    setup_log_and_help();
    determine_version();
    determine_parts();

    run_cli_arguments(*args);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setup_log_and_help():
    global LOG;
    global INFO

    config = Struct.get_from_file('config.yml');
    config_logging = Struct.get_value(config, 'logging', default=dict());
    LOG = Logger(config_logging);
    INFO = Info(LOG);
    return;

def determine_version():
    global LOG;
    global VERSION;

    try:
        VERSION = Info.version;
    except Exception as err:
        VERSION = None;
        LOG.error(str(err));
    return;

def determine_parts():
    global INFO;
    global PARTS;

    PARTS = [];
    for part in INFO.get_attributes('cli', default={}):
        arg = INFO.get_attributes('cli', part, 'key');
        cmd = INFO.get_attributes('cli', part, 'command');
        module = INFO.get_attributes('cli', part, 'module');
        if isinstance(arg, str) and isinstance(cmd, str) and isinstance(module, str):
            PARTS.append((part, cmd, arg, module));
    return;

def run_cli_arguments(*args: str):
    global LOG;
    global VERSION;

    # first extract main arguments
    arguments = INFO.parse_arguments('main');
    arguments.parse(*args);
    argumentValues = INFO.arguments.values;
    if INFO.check_validity(quiet=True):
        LOG.colourmode = argumentValues.getValueAsBoolean('colour');
        LOG.verbose = argumentValues.getValueAsBoolean('verbose');

    # check if the argument is a (sub)programme:
    if len(args) > 0:
        arg_first = args[0];
        for (part, _, arg, module) in PARTS:
            if arg == arg_first:
                run_sub_programme(part, module, *args);
                return;

    # display main options
    if argumentValues.getValueAsBoolean('version'):
        LOG.plain(VERSION or '???');
    elif argumentValues.getValueAsBoolean('help'):
        INFO.console_help('main');
    else:
        # display argument errors, if any
        if not INFO.check_validity(quiet=False):
            return;
        # else, show suggestions
        LOG.info('Try using the argments \033[1;96m--version\033[0m or \033[1;96m--help\033[0m.');
    return;

def run_sub_programme(part: str, module: str, *args: str):
    global LOG;
    global INFO;
    global VERSION;

    arguments = INFO.parse_arguments(part);
    arguments.parse(*args);
    name = INFO.get_name('cli', part);
    argumentValues = INFO.arguments.values

    # otherwise display argument errors, if any
    if argumentValues.getValueAsBoolean('version'):
        LOG.plain('\033[1;32m{name}\033[0m version \033[1;92m{v}\033[0m'.format(name=name, v=VERSION or '???'));
    elif argumentValues.getValueAsBoolean('help'):
        INFO.console_help(part);
    else:
        # display argument errors, if any
        if not INFO.check_validity(quiet=False):
            return;

        # else, command is valid. Attempt to open module:
        if module == 'transpile':
            subprogramme_transpile(LOG, argumentValues);
            return;
        elif module == 'create':
            subprogramme_create(LOG, argumentValues);
            return;
        else:
            LOG.error('The subprogramme \033[1;32m{module}\033[0m has not been implemented.'.format(module=module));
    return;
