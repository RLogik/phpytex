#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;
import re;
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
VERSION: str;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    tokens, kwargs = parse_cli_args(sys.argv[1:]);
    setup_log();
    get_version();
    log.info('At the moment nothing has been implemented.'.format(VERSION));
    run_command(tokens=tokens, **kwargs);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXLIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_version() -> str:
    global VERSION;
    version = None;
    try:
        with open(os.path.join(SOURCEDIRECTORY, 'VERSION')) as fp:
            for line in fp.readlines():
                line = re.sub(r'^[\s\n\r]+|[\s\n\r]+$', r'', line);
                if not re.match(r'^\d+\.\d+\.\d+$', line):
                    continue;
                version = line;
                break;
    except:
        pass;
    if version is None:
        raise ValueError('VERSION file missing in the distribution folder or the value is invalid!');
    VERSION = version;
    return version;

def setup_log():
    global log;
    config = extractConfig(os.path.join(SOURCEDIRECTORY, 'config.yml'));
    config_logging = get_dict_value(config, 'logging', default=dict());
    log = Logger(config_logging);
    return;

def run_command(tokens: List[str], **kwargs):
    global log;
    global VERSION;
    if 'version' in tokens:
        log.info('This is version \033[1;92m{}\033[0m of the \033[1;32m(Ph(P)y)TeX\033[0m programme.'.format(VERSION));
    else:
        log.info('You called this programme with the tokens:   ' + str(tokens) + '.');
        log.info('You called this programme with the keywords: ' + str(kwargs) + '.');
        log.info('Try calling the programme with the argument \033[1;94m--version\033[0m.');
    return;
