#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import re;

from pathlib import Path;
from subprocess import Popen;
from textwrap import dedent;
from typing import Any;
from typing import Dict;
from typing import List;
from typing import Tuple;
from typing import Type;
from typing import Union;

from src.__path__ import PATH_APP_INTERNAL;
from src.core.log import logInfo;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ENCODING_ASCII:   str = 'ascii';
ENCODING_UTF8:    str = 'utf-8';
ENCODING_UNICODE: str = 'unicode_escape';

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
    path = os.path.join(PATH_APP_INTERNAL, path) if internal else path;
    with open(path, 'r') as fp:
        return ''.join(fp.readlines());

def writeTextFile(path: str, lines: str):
    with open(path, 'w') as fp:
        fp.write(lines);

def write_lines(path: str, lines: List[str]):
    with open(path, 'w') as fp:
        for line in lines:
            fp.write(line + '\n');
    return;

def write_file(fname: str, lines: List[str], force_create_path: bool = False, force_create_empty_line: bool = True):
    if force_create_path:
        create_path(os.path.dirname(fname));
    while len(lines) > 0:
        if not re.match(r'^\s*$', lines[-1]):
            break;
        lines = lines[:-1];
    if force_create_empty_line:
        lines = lines + [''];
    with open(fname, 'w+') as fp:
        fp.writelines('\n'.join(lines));
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: string
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def escapeForPython(s: str) -> str:
    s = re.sub(r'(\\+)', r'\1\1', s);
    s = re.sub(r'\n', r'\\n', s);
    s = re.sub(r'\t', r'\\t', s);
    s = re.sub(r'\"', r'\\u0022', s);
    s = re.sub(r'\'', r'\\u0027', s);
    # s = re.sub(r'\%', slash+'u0025', s);
    s = re.sub(r'(\{+)', r'\1\1', s);
    s = re.sub(r'(\}+)', r'\1\1', s);
    return s;

def formatBlockIndent(u: str, indent: str) -> str:
    u = dedent(u);
    lines = u.split('\n');
    linesNew = [];
    for line in lines:
        linesNew.append(indent + line);
    return '\n'.join(linesNew);

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
