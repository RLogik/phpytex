#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import re;

from pathlib import Path;
from platform import system as platformSystem;
from subprocess import Popen;
from subprocess import run as subprocessRun;
from textwrap import dedent;
from typing import Any;
from typing import Dict;
from typing import List;
from typing import Tuple;
from typing import Type;
from typing import Union;

from src.core.path import getAppPath;
from src.core.log import logInfo;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ENCODING_ASCII:   str = 'ascii';
ENCODING_UTF8:    str = 'utf-8';
ENCODING_UNICODE: str = 'unicode_escape';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD os sensitive commands
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def isLinux() -> bool:
    return not ( os.name == 'nt' );

def PythonCommand() -> str:
    return 'python3' if isLinux() else 'py -3';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: io
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def pipeCall(*_args, cwd = None, errormsg: str):
    args = [_ for _ in _args];
    if not isinstance(cwd, str):
        cwd = os.getcwd();
    pipe = Popen(args, cwd=cwd);
    pipe.wait();
    if pipe.returncode == 0:
        return;
    raise Exception(errormsg);

def callPython(fname: str, *args: str, fnameOut: Union[None, str] = None):
    cmd = ['py', '-3'] if platformSystem().lower() == 'windows' else ['python3'];
    cmd = [*cmd, fname, *args];
    if fnameOut is None:
        result = subprocessRun(cmd);
    else:
        with open(fnameOut, 'w') as fp:
            result = subprocessRun(cmd, stdout=fp);
    if not result.returncode == 0:
        raise Exception('The process did not run successfully.');

def getFiles(path: str) -> List[Tuple[str, str]]:
    items = [(_, os.path.join(path, _)) for _ in os.listdir(path)];
    return [ (_, __) for _, __ in items if os.path.isfile(__)];

def getFilesByPattern(path: str, filepattern: str) -> List[str]:
    regex = re.compile(filepattern);
    return [ __ for _, __ in getFiles(path) if regex.match(_) ];

def make_file_if_not_exists(path: str, fname: str) -> bool:
    fname_full = os.path.join(path, fname);
    try:
        if not os.path.isfile(fname_full):
            logInfo('  File \033[96;1m{}\033[0m will be created.'.format(fname));
            Popen(['touch', fname], cwd=path).wait();
            Path(fname_full).touch(exist_ok=True);
    except:
        pass;
    return os.path.isfile(fname_full);

def make_dir_if_not_exists(path: str, fname: str) -> bool:
    fname_full = os.path.join(path, fname);
    try:
        if not os.path.isdir(fname_full):
            logInfo('  Folder \033[96;1m{}\033[0m will be created.'.format(fname));
            Path(fname_full).mkdir(parents=True, exist_ok=True);
    except:
        pass;
    return os.path.isdir(fname_full);

def create_path(path: str):
    if not os.path.exists(path):
        Path(path).mkdir(parents=True, exist_ok=True);
    if not os.path.exists(path):
        raise FileExistsError('Could not create or find path \033[93;1m{}\033[0m!'.format(path));
    return;

def readTextFile(path: str, internal: bool = False) -> str:
    path = os.path.join(getAppPath(), path) if internal else path;
    with open(path, 'r') as fp:
        return ''.join(fp.readlines());

def writeTextFile(
    path: str,
    lines: Union[str, List[str]],
    force_create_path: bool = False,
    force_create_empty_line: bool = True
):
    if force_create_path:
        create_path(os.path.dirname(path));
    _lines = [lines] if isinstance(lines, str) else lines
    while len(_lines) > 0:
        if not re.match(r'^\s*$', _lines[-1]):
            break;
        lines = lines[:-1];
    if force_create_empty_line:
        _lines = _lines + [''];
    with open(path, 'w') as fp:
        fp.write('\n'.join(_lines));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: cli
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getCliArgs(*args: str) -> Tuple[List[str], Dict[str, Any]]:
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
# METHODS: string
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def formatBlockIndent(u: str, indent: str) -> str:
    u = dedent(u);
    lines = u.split('\n');
    linesNew = [];
    for line in lines:
        linesNew.append(indent + line);
    return '\n'.join(linesNew);

def DedentIgnoreFirstAndLast(s: str) -> str:
    s = re.sub(r'(^[\n\r])|([\n\r]$)', '', s);
    return dedent(s);

def formatTextBlock(s: str) -> str:
    return DedentIgnoreFirstAndLast(s);

def formatTextBlockAsList(s: str) -> List[str]:
    return re.split(r'\n', DedentIgnoreFirstAndLast(s));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: yaml and config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def toPythonKeys(key: str) -> str:
    return re.sub(r'-', r'_', key);

def toPythonKeysDict(obj: Dict[str, Any]) -> Dict[str, Any]:
    return { toPythonKeys(key): value for key, value in obj.items() };

def getAttributeIgnoreError(obj: Any, *keys: Union[str, int], expectedtype: Union[Type, Tuple[Type]] = Any, default: Any = None):
    try:
        value = getAttribute(obj, *keys, expectedtype=expectedtype, default=default);
    except:
        value = default;
    return value;

def getAttribute(obj: Any, *keys: Union[str, int], expectedtype: Union[Type, Tuple[Type]] = Any, default: Any = None) -> Any:
    if len(keys) == 0:
        return obj;
    key = keys[0];
    try:
        if isinstance(key, str) and isinstance(obj, dict) and key in obj:
            value = obj[key];
            if len(keys) <= 1:
                return value if isinstance(value, expectedtype) else default;
            else:
                return getAttribute(obj[key], *keys[1:], expectedtype=expectedtype, default=default);
        elif isinstance(key, int) and isinstance(obj, (list,tuple)) and key < len(obj):
            value = obj[key];
            if len(keys) <= 1:
                return value if isinstance(value, expectedtype) else default;
            else:
                return getAttribute(obj[key], *keys[1:], expectedtype=expectedtype, default=default);
    except:
        pass;
    if len(keys) <= 1:
        return default;
    path = ' -> '.join([ key if isinstance(key, str) else '[{}]'.format(key) for key in keys ]);
    raise Exception('Could not find \033[1m{}\033[0m in object!'.format(path));
