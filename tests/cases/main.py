#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
import sys

os.chdir(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.getcwd())

import logging

from src.thirdparty.config import *
from src.thirdparty.misc import *
from src.thirdparty.system import *
from src.thirdparty.types import *

from src.setup import *
from src._core.logging import *
from src.models.application import *
from src.models.generated.tests import *
from src.queries.console.cases import *
from src.features import *

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

PID = os.getpid()
PATTERN_CASE: str = r'^(case|private_).*'
PATH_SCRIPT: str = f'src.main'
PATH_CASES: str = f'tests/cases'
PATH_CONFIG: str = f'{PATH_CASES}/config.yaml'
PATH_SANDBOX: str = f'{PATH_CASES}/sandbox'

# ----------------------------------------------------------------
# EXECUTION
# ----------------------------------------------------------------

if __name__ == '__main__':
    sys.tracebacklimit = 0
    config.open_source.set(False)
    args = CliArguments(config.INFO, config.APPCONFIG).parse(*sys.argv[1:])

    if args.mode == EnumProgrammeMode.VERSION:
        print(config.VERSION)
        exit(0)

    config.pid.set(PID)
    config.path_logging.set(args.log)
    config.quiet_mode.set(args.quiet)
    config.initialise_application(name='tests', debug=args.debug)

    with open(PATH_CONFIG, 'rb') as fp:
        assets = yaml.load(fp, yaml.FullLoader)
        cfg = TestCaseConfig.model_validate(assets)

    remove_dir_if_exists(PATH_SANDBOX)
    message_pause = f'Output can be temporarily inspected in \033[1m{PATH_SANDBOX}\033[0m'
    for path in cfg.cases:
        shutil.copytree(src=path, dst=PATH_SANDBOX)
        cmd = re.split(r'\s+', python_command())

        try:
            pipe_call(
                [
                    *cmd,
                    '-m',
                    PATH_SCRIPT,
                    '--path',
                    PATH_SANDBOX,
                    '--log',
                    args.log,
                    'run',
                    'TRANSPILE',
                ],
                cwd=os.getcwd(),
            )
        except BaseException as err:
            err.add_note(f'Test case \033[1m{path}\033[0m failed.')
            if args.inspect:
                logging.error('An error occurred', err, message_pause)
                input('Press any key to continue...')
            raise err

        if args.inspect:
            logging.debug(message_pause)
            input('Press any key to continue...')

        remove_dir_if_exists(PATH_SANDBOX)
