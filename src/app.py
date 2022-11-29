#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))));

from src.thirdparty.config import *;
from src.thirdparty.system import *;

from src.setup import *;
from src.core.log import *;
from src.models.cli import *;
from src.models.internal import *;
from src.endpoints import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'enter',
    'check_python_version',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PYTHON_VERSION_MINIMUM = (3, 10);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN PROCESS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def enter(
    path_root: str,
    path_app:  str,
    args: ProgrammeArguments,
):
    # set paths:
    config.FILE_OPTIONS.path_app = path_app;
    config.FILE_OPTIONS.path_root = path_root;

    # set logging level, colour, quiet mode:
    set_ansi_mode(args.colour);
    set_debug_mode(args.debug);
    set_quiet_mode(args.quiet);

    # choose subprogramme:
    match args.mode:
        case EnumProgrammeMode.version:
            endpoint_display_version();
        case EnumProgrammeMode.help:
            endpoint_display_help();
        case EnumProgrammeMode.run:
            parameters = json_load_safe(args.parameters);
            endpoint_run_phpytex(fnameConfig=args.file, parameters=parameters);
        case _:
            display_usage();
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY PROCESSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def check_python_version() -> None:
    major, minor = [ int(n) for n in platform.python_version_tuple()[:2] ];
    if major > PYTHON_VERSION_MINIMUM[0] or (major == PYTHON_VERSION_MINIMUM[0] and minor >= PYTHON_VERSION_MINIMUM[1]):
        return;
    version = platform.python_version();
    raise Exception(f'Python version is {version}, but must be at least {PYTHON_VERSION_MINIMUM[0]}.{PYTHON_VERSION_MINIMUM[1]}.*.');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    # sys.tracebacklimit = 0;
    check_python_version();
    args = get_arguments_from_cli(*sys.argv[1:]);
    open_source(True);
    path_root = os.getcwd();
    path_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
    enter(path_root=path_root, path_app=path_app, args=args);
