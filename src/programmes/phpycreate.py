#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import List;

from ..core.logger import Logger;
from ..info.info import Help;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LOG: Logger;
HELP: Help;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(log: Logger, version: str, *tokens: str, **kwargs):
    global LOG;
    global HELP;
    global VERSION;

    LOG = log;
    HELP = Help(LOG);
    VERSION = version;

    run_cli_arguments(list(tokens), **kwargs);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECUNDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_cli_arguments(tokens: List[str], **kwargs):
    global LOG;
    global HELP;
    global VERSION;

    if 'version' in tokens:
        LOG.plain('\033[1;32m(Ph(P)y)create\033[0m version \033[1;92m{}\033[0m'.format(VERSION or '???'));
    elif 'help' in tokens:
        HELP.console_help('create');
    else:
        LOG.info('Methods for \033[1;32m(Ph(P)y)create\033[0m version \033[1;92m{}\033[0m are under construction.'.format(VERSION));
        LOG.info('Try calling \033[1;96mphpytex --create\033[0m [\033[1;96m--version\033[0m|\033[1;96m--help\033[0m].');
    return;
