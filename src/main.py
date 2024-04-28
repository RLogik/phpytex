#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from .thirdparty.system import *

from .setup import *
from .models.application import *
from .queries.console.client import *
from .features import *

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

    run.process(feature=args.feature, path_config=args.config, parameters=args.parameters or {})
