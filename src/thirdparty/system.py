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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODIFICATIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_dir_if_not_exists(path: str) -> None:
    '''
    Creates a directory if it does not exist.
    '''
    if not os.path.exists(path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True);
    if not os.path.exists(path) or not os.path.isdir(path):
        raise FileExistsError(f'\033[93;1m{path}\033[0m could not be created!');
    return;

def create_file_if_not_exists(path: str) -> None:
    '''
    Creates a file if it does not exist.
    '''
    if not os.path.exists(path):
        pathlib.Path(path).touch(exist_ok=True);
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileExistsError(f'\033[93;1m{path}\033[0m could not be created!');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'os',
    'pathlib',
    'platform',
    'shutil',
    'subprocess',
    'sys',
    'create_dir_if_not_exists',
    'create_file_if_not_exists',
];
