#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;
import pathlib;
import platform;
import shutil;
import subprocess;

import re;
from typing import Optional;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODIFICATIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_full_path(path: str, shouldexist: bool = False) -> str:
    path = os.path.abspath(path);
    if shouldexist and not os.path.exists(path):
        raise Exception(f'Path \033[1m{path}\033[0m does not exist!');
    return path;

def format_path(
    path: str,
    root: str,
    relative: bool,
    ext: Optional[str] = None,
    ext_if_empty: Optional[str] = None,
) -> str:
    if os.path.isabs(path):
        if relative:
            path = os.path.relpath(path=path, start=root);
    else:
        if not relative:
            path = os.path.abspath(os.path.join(root, path));
    path_, ext_ = os.path.splitext(path);
    if ext is not None:
        path = f'{path_}{ext}';
    elif ext_ == '' and ext_if_empty is not None:
        path = f'{path_}{ext_if_empty}';
    return path;

def get_files(path: str) -> list[tuple[str, str]]:
    items = [(_, os.path.join(path, _)) for _ in os.listdir(path)];
    return [ (_, __) for _, __ in items if os.path.isfile(__)];

def get_files_by_pattern(path: str, pattern: str) -> list[str]:
    regex = re.compile(pattern);
    return [ __ for _, __ in get_files(path) if regex.match(_) ];

def create_new_path_name(dir: str, nameinit: str = 'tmp', namescheme: str = 'tmp_{}') -> str:
    '''
    Creates a new path name. Uses template if path already exists.
    '''
    path = os.path.join(dir, nameinit);
    i = 0;
    while os.path.isdir(path):
        path = os.path.join(dir, namescheme.format(i));
        i += 1;
    return path;

def create_new_file_name(dir: str, nameinit: str = 'tmp', namescheme: str = 'tmp_{}') -> str:
    '''
    Creates a new file name. Uses template if file already exists.
    '''
    path = os.path.join(dir, nameinit);
    i = 0;
    while os.path.isfile(path):
        path = os.path.join(dir, namescheme.format(i));
        i += 1;
    return path;

def create_file_if_not_exists(path: str) -> None:
    '''
    Creates a file if it does not exist.
    '''
    if not os.path.exists(path):
        pathlib.Path(path).touch(exist_ok=True);
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileExistsError(f'\033[93;1m{path}\033[0m could not be created!');
    return;

def create_dir_if_not_exists(path: str) -> None:
    '''
    Creates a directory if it does not exist.
    '''
    if path in [ '', '.', os.getcwd() ]:
        return;
    if not os.path.exists(path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True);
    if not os.path.exists(path) or not os.path.isdir(path):
        raise FileExistsError(f'\033[93;1m{path}\033[0m could not be created!');
    return;

def read_text_file(path: str) -> str:
    '''
    Reads from text file.
    '''
    with open(path, 'r') as fp:
        return ''.join(fp.readlines());

def write_text_file(
    path: str,
    lines: str | list[str],
    force_create_path: bool = False,
    force_create_empty_line: bool = True
):
    '''
    Writes text to a file (overwrites if already exists).
    '''
    if force_create_path:
        create_dir_if_not_exists(os.path.dirname(path));
    if isinstance(lines, str):
        text = lines.rstrip('\r\n');
    else:
        while len(lines) > 0:
            if not re.match(pattern=r'^\s*$', string=lines[-1]):
                break;
            lines = lines[:-1];
        text = '\n'.join(lines);
    with open(path, 'w') as fp:
        fp.write(text);
        if force_create_empty_line:
            fp.write('\n');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'create_dir_if_not_exists',
    'create_file_if_not_exists',
    'create_new_file_name',
    'create_new_path_name',
    'format_path',
    'get_files_by_pattern',
    'get_files',
    'get_full_path',
    'os',
    'pathlib',
    'platform',
    'read_text_file',
    'shutil',
    'subprocess',
    'sys',
    'write_text_file',
];
