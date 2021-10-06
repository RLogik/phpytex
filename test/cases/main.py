#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

PATH_PROJECT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)));
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

PATH_CASES:   str = 'test/cases';
PATTERN_CASE: str = r'^(case|private_).*';
PATH_CONFIG:  str = 'test/cases/setup/config.yml';
PATH_SCRIPT:  str = os.path.join(PATH_PROJECT, 'src', 'main.py');
PATH_SANDBOX: str = os.path.join(PATH_CASES, 'sandbox');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN PROCESS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(*tokens, **kwargs):
    inspect = ( 'inspect' in tokens );

    config = StepGetConfig(PATH_CONFIG);
    paths = getAttribute(config, 'cases', expectedtype=list, default=[]);
    cases = StepGetTestCases(PATH_CASES, PATTERN_CASE);
    ClearSandbox(PATH_SANDBOX);
    for path in cases:
        if not (path in paths):
            continue;
        logPlain('');
        StepRunTestCase(path=path, sandboxpath=PATH_SANDBOX, phpytex_script=PATH_SCRIPT, inspect=inspect);
        ClearSandbox(PATH_SANDBOX);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY PROCESSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def StepGetConfig(path_config: str) -> Dict[str, Any]:
    return readYamlFile(path_config);

def ClearSandbox(sandboxpath: str):
    if os.path.isdir(sandboxpath):
        subprocess.run(['rm', '-rf', sandboxpath]);
    return;

def StepGetTestCases(path_cases: str, pattern: str) -> List[str]:
    cases = [];
    for path in os.listdir(path_cases):
        path_full = os.path.join(path_cases, path);
        if not os.path.isdir(path_full):
            continue;
        if not re.match(pattern, path):
            continue;
        cases.append(path_full);
    cases = sorted(cases);
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
    try:
        pipeCall(*cmd, phpytex_script, 'run', cwd=sandboxpath);
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
    return os.path.relpath(path, start=PATH_PROJECT);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 0;
    tokens, kwargs = getCliArgs(*sys.argv[1:]);
    main(*tokens, **kwargs);
