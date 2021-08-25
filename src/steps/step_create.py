#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import re
from src.core.log import logInfo;
from src.setup import appconfig;
from typing import Any;
from typing import Dict;
from typing import List;

from src.core.utils import getAttribute;
from src.core.utils import make_file_if_not_exists;
from src.core.utils import make_dir_if_not_exists;
from src.core.utils import writeTextFile;
from src.setup import appconfig;
from src.parsers.methods import convertToPythonString;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step create
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step(
    stamp:      Dict[str, Any] = dict(),
    parameters: Dict[str, Any] = dict(),
    files:      List[str]      = [],
    folders:    Dict[str, Any] = dict(),
    **_
):
    createFilesAndFolders(path=appconfig.getWorkingDirectory(), files=files, folders=folders);
    createFileStamp(**stamp);
    createFileParameters(**parameters);
    logInfo('Creation stage complete.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def createFilesAndFolders(
    path: str,
    files: List[str],
    folders: Dict[str, Any],
    **_
):
    for fname in files:
        if not make_file_if_not_exists(path=path, fname=fname):
            raise FileExistsError('Could not create file \033[1m{}\033[0m'.format(os.path.join(path, fname)));
    for subfolder in folders:
        _path = os.path.join(path, subfolder);
        if not make_dir_if_not_exists(path=path, fname=subfolder):
            raise FileExistsError('Could not create (sub)folder \033[1m{}\033[0m'.format(_path));
    for subfolder in folders:
        _path = os.path.join(path, subfolder);
        _files = getAttribute(folders[subfolder], 'files', expectedtype=list, default=[]);
        _folders = getAttribute(folders[subfolder], 'folders', expectedtype=dict, default=dict());
        createFilesAndFolders(path=_path, files=_files, folders=_folders);
    return;

def createFileStamp(
    file: str,
    overwrite: bool = False,
    options: Dict[str, Any] = dict(),
    **_
):
    appconfig.setStampFile(file);
    path = os.path.join(appconfig.getWorkingDirectory(), file);
    if os.path.isfile(path) and not overwrite:
        return;
    lines = [];
    border = r'%% ' + '*'*80;
    max_tag_length = max([0] + [len(key) for key in options]);
    for key in options:
        value = options[key];
        tag = key.upper();
        line = r'%% ' + tag + r':';
        if isinstance(value, str):
            value = re.split('\n', str(value));
        elif isinstance(value, (int, float, bool)):
            value = [str(value)];
        if isinstance(value, list) and len(value) == 1:
            line += ' '*(1 + max_tag_length - len(tag)) + str(value[0]);
        elif isinstance(value, list) and len(value) > 1:
            indent = '\n' + r'%% ' + ' '*4;
            line_ = [''];
            line_ += [u for u in value if isinstance(u, str)];
            line += indent.join(line_);
        else:
            line += ' '*(1 + max_tag_length - len(tag)) + r'—';
        lines.append(line);
    if len(lines) > 0:
        lines = [border] + lines + [border];
    writeTextFile(path=path, lines=lines);
    return;

def createFileParameters(
    file: str = '',
    overwrite: bool = True,
    options: Dict[str, Any] = dict(),
    **_
):
    global PARAMDATEI;
    PARAMDATEI = file;
    path = os.path.join(appconfig.getWorkingDirectory(), file);
    if os.path.isfile(path) and not overwrite:
        return;
    lines = [];
    for key in options:
        try:
            typ, value = convertToPythonString(options[key], indent=0, multiline=False);
            lines.append('<<< set global {key} = {value}; >>>'.format(
                key   = key,
                value = value,
            ));
        except:
            continue;
    writeTextFile(path=path, lines=lines);
    return;
