#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;
from typing import List;
from typing import Union;

from .core.config import Struct;
from .core.logger import Logger;
from .core.utils import parse_cli_args;
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
PARTS: List[List[str]];

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
        arg = INFO.get_attributes('cli', part, 'key', default=part);
        cmd = INFO.get_attributes('cli', part, 'command', default=part);
        PARTS.append([part, arg, cmd]);
    return;

def run_cli_arguments(*args: str):
    global LOG;
    global VERSION;

    # check if the argument is a (sub)programme:
    if len(args) > 0:
        arg_first = args[0];
        for [part, arg, _] in PARTS:
            if arg == arg_first:
                run_sub_programme(part, *args);
                return;

    # if not, then only limitted functionality available:
    tokens, _, _ = parse_cli_args(*args, strict=False, ignorecase=True);
    if 'version' in tokens:
        LOG.plain(VERSION or '???');
    elif 'help' in tokens:
        LOG.info('Try calling ' + ', '.join(['\033[1;96m{} --help\033[0m'.format(cmd) for [_, _, cmd] in PARTS]) + '.');
    else:
        LOG.info('Try using the argments \033[1;96m--version\033[0m or \033[1;96m--help\033[0m.');
    return;

def run_sub_programme(part: str, *args: str):
    global LOG;
    global INFO;
    global VERSION;

    arguments = INFO.parse_arguments(part);
    arguments.parse(*args);
    module = INFO.get_attributes('cli', part, 'module', default=part);
    name = INFO.get_name('cli', part);

    if 'version' in arguments.tokens:
        LOG.plain('\033[1;32m{name}\033[0m version \033[1;92m{v}\033[0m'.format(name=name, v=VERSION or '???'));
    elif 'help' in arguments.tokens or 'man' in arguments.tokens:
        INFO.console_help(part);
    else:
        cli_validity = INFO.check_validity(quiet=False);
        if not cli_validity:
            return;
        ## From this point the CLI command is valid and the subprogramme can run.
        argumentValues = INFO.arguments.values
        if module == 'transpile':
            subprogramme_transpile(LOG, argumentValues);
            return;
        elif module == 'create':
            subprogramme_create(LOG, argumentValues);
            return;
        else:
            LOG.error('The subprogramme \033[1;32m{module}\033[0m has not been implemented.'.format(module=module));
    return;
