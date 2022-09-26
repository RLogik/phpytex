#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'));
sys.path.insert(0, os.getcwd());

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

PATTERN_CASE: str = r'^(case|private_).*';
PATH_SCRIPT:  str = f'{os.getcwd()}/src/main.py';
PATH_CASES:   str = f'{os.getcwd()}/tests/cases';
PATH_CONFIG:  str = f'{PATH_CASES}/config.yml';
PATH_SANDBOX: str = f'{PATH_CASES}/sandbox';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN PROCESS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(*tokens, **kwargs):
    inspect = ( 'inspect' in tokens );
    config = StepGetConfig(PATH_CONFIG);
    paths = getAttribute(config, 'cases', expectedtype=list, default=[]);
    # cases = StepGetTestCases(PATH_CASES, PATTERN_CASE);
    ClearSandbox(PATH_SANDBOX);
    for path in paths:
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
    inspect:        bool,
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
    return os.path.relpath(path, start=os.getcwd());

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 0;
    tokens, kwargs = getCliArgs(*sys.argv[1:]);
    main(*tokens, **kwargs);
