#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

os.chdir(os.path.join(os.path.dirname(__file__), '..'));
sys.path.insert(0, os.getcwd());

from src.thirdparty.misc import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.core.log import *;
from src.core.utils import *;
from tests.setup import *;
from tests.models.cli import *;
from tests.endpoints import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATTERN_CASE: str = r'^(case|private_).*';
PATH_SCRIPT:  str = f'{os.getcwd()}/src/app.py';
PATH_CASES:   str = f'{os.getcwd()}/tests/cases';
PATH_CONFIG:  str = f'{PATH_CASES}/config.yaml';
PATH_SANDBOX: str = f'{PATH_CASES}/sandbox';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN PROCESS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def enter(args: ProgrammeArguments):
    set_ansi_mode(args.colour);
    set_debug_mode(args.debug);
    set_quiet_mode(args.quiet);

    match args.mode:
        case EnumProgrammeMode.run:
            for case in tests_config.CASES:
                endpoint_test_case(case=case, inspect=args.inspect);
        case EnumProgrammeMode.help:
            endpoint_display_help();
        case _:
            display_usage();
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    args = get_arguments_from_cli(*sys.argv[1:]);
    enter(args);
