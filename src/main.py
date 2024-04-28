#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
import sys

# NOTE: do not change the directory!
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.thirdparty.system import *

from src.setup import *
from src.models.application import *
from src.queries.console.client import *
from src.features import *

# ----------------------------------------------------------------
# LOCAL CONSTANTS
# ----------------------------------------------------------------

PID = os.getpid()

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
    config.initialise_application(name='app', debug=args.debug)

    # set working directory to user option if set
    if args.path is not None:
        os.chdir(args.path)

    run.process(
        feature=args.feature,
        path_config=args.config,
        compileoptions=args.compile or {},
        parameters=args.parameters or {},
    )
