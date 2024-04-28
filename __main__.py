#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the entry point script
needed for the created artefact.

NOTE: The imports in this files have to be absolute.
The modules however may use relative imports.
'''

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

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
    config.open_source.set(True)
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
