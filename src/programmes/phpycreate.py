#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import List;
from typing import Union;

from ..core.logger import Logger;
from ..info.info import Help;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LOG: Logger;
HELP: Help;
VERSION: Union[str, None] = None;
PART: str = 'create';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(log: Logger, version: str, *args: str):
    global LOG;
    global HELP;
    global VERSION;
    global PART;

    LOG = log;
    HELP = Help(LOG);
    VERSION = version;

    run_cli_arguments(*args);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECUNDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_cli_arguments(*args: str):
    global LOG;
    global HELP;
    global VERSION;
    global PART;

    arguments = HELP.get_cli_structure(PART);
    arguments.parse(*args);

    if 'version' in arguments.tokens:
        LOG.plain('\033[1;32m(Ph(P)y)create\033[0m version \033[1;92m{}\033[0m'.format(VERSION or '???'));
    elif 'help' in arguments.tokens:
        HELP.console_help(PART);
    else:
        LOG.info('Methods for \033[1;32m(Ph(P)y)create\033[0m version \033[1;92m{}\033[0m are under construction.'.format(VERSION));
        LOG.info('Try calling \033[1;96mphpytex --create\033[0m [\033[1;96m--version\033[0m|\033[1;96m--help\033[0m].');
        LOG.info('You used the cli-argument {}'.format(arguments));
    return;
