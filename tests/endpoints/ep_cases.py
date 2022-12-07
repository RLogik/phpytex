#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.system import *;

import tests.paths;
from src.setup import *;
from src.core.log import *;
from src.core.utils import *;
from tests.setup import *;
from tests.models.config import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'endpoint_test_case',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENDPOINT run test case
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def endpoint_test_case(
    case: TestCase,
    inspect: bool,
) -> None:
    sandbox_path = tests_config.PATHS.path_sandbox;

    log_plain('');
    log_info('START TEST CASE');
    log_info(f'path = \x1b[1m{case.path}\x1b[0m'.format());

    try:
        remove_folder(sandbox_path);
        copy_folder(src=case.path, dst=sandbox_path);
        run_test();
    except:
        log_fatal(f'Test case \x1b[1m{case.path}\x1b[0m failed.');

    if inspect:
        log_debug(f'Output can be temporarily inspected in \x1b[1m{sandbox_path}\x1b[0m')
        input('Press any key to continue...');

    remove_folder(sandbox_path);
    log_info('END TEST CASE');
    return;

def run_test() -> None:
    sandbox_path = tests_config.PATHS.path_sandbox;
    cmd = python_command_split();
    pipeCall(*cmd, tests.paths.programme, 'run', cwd=sandbox_path);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def copy_folder(src: str, dst: str) -> None:
    shutil.copytree(src=src, dst=dst);
    return;

def remove_folder(path: str):
    if os.path.isdir(path):
        subprocess.run(['rm', '-rf', path]);
    return;
