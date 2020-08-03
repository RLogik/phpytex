#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;
sys.tracebacklimit = 0; ## disables traceback.
from typing import List;
from typing import Tuple;
from typing import Union;

from .values.struct import Struct;
from .core.logger import LoggerService;
from .info.information import InformationService;
from .programmes.transpile.main import main as subprogramme_transpile;
from .programmes.create.main import main as subprogramme_create;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WORKINGDIRECTORY = os.getcwd();
LOG: LoggerService;
INFO: InformationService;
VERSION: Union[str, None] = None;
SUBPROGRAMMES: List[Tuple[str, str, str, str, str]];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    args = sys.argv[1:];

    setup_log_and_help();
    determine_version();
    determine_subprogrammes();

    run_cli_arguments(*args);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setup_log_and_help():
    global LOG;
    global INFO

    config = Struct(fname=os.path.join('setup', 'config.yml'), internal=True);
    config_logging = config.getSubStruct('configuration', 'logging');
    LOG = LoggerService(config_logging);
    INFO = InformationService(spec=config, log=LOG);
    return;

def determine_version():
    global LOG;
    global VERSION;

    try:
        VERSION = InformationService.version;
    except Exception as err:
        VERSION = None;
        LOG.error(str(err));
    return;

def determine_subprogrammes():
    global INFO;
    global SUBPROGRAMMES;

    SUBPROGRAMMES = [];
    for prog in INFO.get_attributes('programmes', default={}):
        arg = INFO.get_attributes('programmes', prog, 'key');
        cmd = INFO.get_attributes('programmes', prog, 'command');
        module = INFO.get_attributes('programmes', prog, 'module');
        logname = INFO.get_attributes('programmes', prog, 'logname');
        if isinstance(arg, str) and isinstance(cmd, str) and isinstance(module, str):
            SUBPROGRAMMES.append((prog, cmd, arg, logname, module));
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
        for (prog, _, arg, logname, module) in SUBPROGRAMMES:
            if arg == arg_first:
                run_sub_programme(prog, logname, module, *args);
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

def run_sub_programme(prog: str, logname: str, module: str, *args: str):
    global LOG;
    global INFO;
    global VERSION;

    LOG.entryname = logname;
    arguments = INFO.parse_arguments(prog);
    arguments.parse(*args);
    name = INFO.get_name('programmes', prog);
    argumentValues = INFO.arguments.values

    # otherwise display argument errors, if any
    if argumentValues.getValueAsBoolean('version'):
        LOG.plain('\033[1;32m{name}\033[0m version \033[1;92m{v}\033[0m'.format(name=name, v=VERSION or '???'));
    elif argumentValues.getValueAsBoolean('help'):
        INFO.console_help(prog);
    else:
        # display argument errors, if any
        if not INFO.check_validity(quiet=False):
            return;

        # else, command is valid. Attempt to open module:
        config = Struct(struct=INFO.struct.getValue('configuration'), internal=True);
        if module == 'transpile':
            subprogramme_transpile(LOG, config, argumentValues);
            return;
        elif module == 'create':
            subprogramme_create(LOG, config, argumentValues);
            return;
        else:
            LOG.error('The subprogramme \033[1;32m{module}\033[0m has not been implemented.'.format(module=module));
    return;
