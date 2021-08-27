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
from src.core.utils import createNewPathName;
from src.core.utils import pipeCall;
from src.core.utils import PythonCommand;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN PROCESS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    phpytex_script = os.path.join(_project_path, 'src', 'main.py');
    cases = StepGetTestCases();
    for path, sandboxpath in cases:
        StepRunTestCase(path, sandboxpath, phpytex_script);
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
        if not re.match(r'^case.*', path):
            continue;
        path_full = os.path.join(_test_path, path);
        cases.append((path_full, sandboxpath));
    return cases;

def StepRunTestCase(path: str, sandboxpath: str, phpytex_script: str):
    logInfo('TEST CASE - {}'.format(path));
    shutil.copytree(src=path, dst=sandboxpath);

    cmd = re.split(r'\s+', PythonCommand());
    pipeCall(*cmd, phpytex_script, cwd=sandboxpath);

    logInfo('TEST CASE - {} - complete'.format(path));
    input('Press any key to continue...');
    subprocess.run(['rm', '-rf', sandboxpath]);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 4;
    main();
