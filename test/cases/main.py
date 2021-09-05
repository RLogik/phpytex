#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys;
import os;
import re;
import shutil;
from typing import List;
from typing import Tuple;
import subprocess;

_project_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)));
_test_path = os.path.dirname(__file__);

os.chdir(_test_path);
sys.path.insert(0, _project_path);

from src.core.log import *;
from src.core.utils import getCliArgs;
from src.core.utils import createNewPathName;
from src.core.utils import pipeCall;
from src.core.utils import PythonCommand;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATTERN_CASE: str = r'^case.*';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN PROCESS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(*tokens, **kwargs):
    inspect = ( 'inspect' in tokens );
    phpytex_script = os.path.join(_project_path, 'src', 'main.py');
    cases = StepGetTestCases();
    for path, sandboxpath in cases:
        logPlain('');
        StepRunTestCase(path=path, sandboxpath=sandboxpath, phpytex_script=phpytex_script, inspect=inspect);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY PROCESSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def StepGetTestCases() -> List[Tuple[str, str]]:
    cases = [];
    sandboxpath = createNewPathName(dir=os.getcwd(), nameinit='sandbox', namescheme='sandbox_{}');
    for path in os.listdir(os.getcwd()):
        if not os.path.isdir(path):
            continue;
        if not re.match(PATTERN_CASE, path):
            continue;
        path_full = os.path.join(_test_path, path);
        cases.append((path_full, sandboxpath));
    cases = sorted(cases, key=lambda x: x[0]);
    return cases;

def StepRunTestCase(
    path:           str,
    sandboxpath:    str,
    phpytex_script: str,
    inspect:        bool
):
    logInfo('START TEST CASE');
    logInfo('path = \033[1m{}\033[0m'.format(getRelPath(path)));

    shutil.copytree(src=path, dst=sandboxpath);
    cmd = re.split(r'\s+', PythonCommand());
    pipeCall(*cmd, phpytex_script, cwd=sandboxpath);

    if inspect:
        logDebug('Output can be temporarily inspected in \033[1m{}\033[0m'.format(getRelPath(sandboxpath)))
        input('Press any key to continue...');
    logInfo('END TEST CASE');
    subprocess.run(['rm', '-rf', sandboxpath]);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TERTIARY PROCESSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getRelPath(path: str) -> str:
    return os.path.relpath(path, start=_project_path);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 4;
    tokens, kwargs = getCliArgs(*sys.argv[1:]);
    main(*tokens, **kwargs);
