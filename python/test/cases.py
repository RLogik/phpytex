#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

PATH_PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
os.chdir(PATH_PROJECT);
sys.path.insert(0, PATH_PROJECT);

from src.local.misc import *;
from src.local.system import *;
from src.local.typing import *;

from src.core.log import *;
from src.core.utils import getAttribute;
from src.core.utils import getCliArgs;
from src.core.utils import pipeCall;
from src.core.utils import PythonCommand;
from src.core.utils import readYamlFile;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CONFIG = None;
PATH_APP = None;
PATH_CASES = None;
PATH_CONFIG = None;
PATH_DIR = None;
PATH_SANDBOX = None;
PATTERN_CASE: str = r'^(case|private_).*';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN PROCESS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(dir: str, app: str, config: str, cases: str, inspect: bool = False, **_):
    global PATH_APP;
    global PATH_CASES;
    global PATH_CONFIG;
    global PATH_DIR;
    global PATH_SANDBOX;

    PATH_DIR = dir;
    PATH_APP = app;
    PATH_CONFIG = config;
    PATH_CASES = cases;
    PATH_SANDBOX = os.path.join(PATH_CASES, 'sandbox');

    StepGetConfig(config);
    paths = getAttribute(CONFIG, 'cases', expectedtype=list, default=[]);
    ClearSandbox(PATH_SANDBOX);
    for path in paths:
        logPlain('');
        StepRunTestCase(
            path        = os.path.join(PATH_CASES, path),
            sandboxpath = PATH_SANDBOX,
            app_path    = PATH_APP,
            inspect     = inspect
        );
        ClearSandbox(PATH_SANDBOX);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY PROCESSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def StepGetConfig(path_config: str) -> Dict[str, Any]:
    global CONFIG;
    CONFIG = readYamlFile(path_config);
    return;

def ClearSandbox(sandboxpath: str):
    if os.path.isdir(sandboxpath):
        subprocess.run(['rm', '-rf', sandboxpath]);
    return;

def StepRunTestCase(
    path:        str,
    sandboxpath: str,
    app_path:    str,
    inspect:     bool
):
    logInfo('START TEST CASE');
    logInfo('path = \033[1m{}\033[0m'.format(getRelPath(path)));

    shutil.copytree(src=path, dst=sandboxpath);
    # cmd = re.split(r'\s+', PythonCommand());
    try:
        pipeCall(app_path, 'run', cwd=sandboxpath);
    except:
        logFatal('Test case \033[1m{}\033[0m failed.'.format(getRelPath(path)));

    if inspect:
        logDebug('Output can be temporarily inspected in \033[1m{}\033[0m'.format(getRelPath(sandboxpath)))
        input('Press any key to continue...');
    logInfo('END TEST CASE');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TERTIARY PROCESSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getRelPath(path: str) -> str:
    return os.path.relpath(path, start=PATH_DIR);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 0;
    tokens, kwargs = getCliArgs(*sys.argv[1:]);
    main(**kwargs, **{ token: True for token in tokens });
