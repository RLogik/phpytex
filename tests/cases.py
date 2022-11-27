#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'));
sys.path.insert(0, os.getcwd());

from src.thirdparty.misc import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.core.log import *;
from src.core.utils import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATTERN_CASE: str = r'^(case|private_).*';
PATH_SCRIPT:  str = f'{os.getcwd()}/src/main.py';
PATH_CASES:   str = f'{os.getcwd()}/tests/cases';
PATH_CONFIG:  str = f'{PATH_CASES}/config.yaml';
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
        log_plain('');
        StepRunTestCase(path=path, sandboxpath=PATH_SANDBOX, phpytex_script=PATH_SCRIPT, inspect=inspect);
        ClearSandbox(PATH_SANDBOX);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY PROCESSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def StepGetConfig(path_config: str) -> dict[str, Any]:
    return readYamlFile(path_config);

def ClearSandbox(sandboxpath: str):
    if os.path.isdir(sandboxpath):
        subprocess.run(['rm', '-rf', sandboxpath]);
    return;

def StepGetTestCases(path_cases: str, pattern: str) -> list[str]:
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
    log_info('START TEST CASE');
    log_info('path = \033[1m{}\033[0m'.format(getRelPath(path)));

    shutil.copytree(src=path, dst=sandboxpath);
    cmd = re.split(r'\s+', PythonCommand());
    try:
        pipeCall(*cmd, phpytex_script, 'run', cwd=sandboxpath);
    except:
        log_fatal('Test case \033[1m{}\033[0m failed.'.format(getRelPath(path)));

    if inspect:
        log_debug('Output can be temporarily inspected in \033[1m{}\033[0m'.format(getRelPath(sandboxpath)))
        input('Press any key to continue...');
    log_info('END TEST CASE');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TERTIARY PROCESSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getRelPath(path: str) -> str:
    return os.path.relpath(path, start=os.getcwd());

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TODO: replace by argparse method
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_cli_args(*args: str) -> tuple[list[str], dict[str, Any]]:
    tokens = [];
    kwargs = {};
    N = len(args);
    indexes = [ i for i, arg in enumerate(args) if re.match(r'^\-+', arg) ];
    notindexes = [ i for i, _ in enumerate(args) if not (i in indexes) ];
    i = 0;
    while i < N:
        if i in indexes and i+1 in notindexes:
            key = re.sub(r'^\-*', '', args[i]).lower();
            value = args[i+1];
            kwargs[key] = value;
            i += 2;
            continue;
        m = re.match(r'^-*(.*?)\=(.*)$', args[i]);
        if m:
            key = re.sub(r'^\-*', '', m.group(1)).lower();
            value = m.group(2);
            kwargs[key] = value;
        else:
            arg = re.sub(r'^\-*', '', args[i]).lower();
            tokens.append(arg);
        i += 1;
    return tokens, kwargs;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 0;
    tokens, kwargs = get_cli_args(*sys.argv[1:]);
    main(*tokens, **kwargs);
