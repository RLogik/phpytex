#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.setup import *;
from src.core.log import *;
from src.core.utils import *;
from src.models.internal import *;
from src.models.user import *;
from src.parsers import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step create
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step():
    log_info('CREATION STAGE STARTED.');
    root = appconfig.getPathRoot();
    createFilesAndFolders(path=root, projectTree=appconfig.getProjectTree());
    if appconfig.getWithFileStamp():
        createFileStamp(
            path=appconfig.getFileStamp(rel=False),
            overwrite=appconfig.getOptionOverwriteStamp(),
            options=appconfig.getDictionaryStamp()
        );
    if appconfig.getWithFileParamsPy():
        createParameters(options=appconfig.getDictionaryParms());
    log_info('CREATION STAGE COMPLETE.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def createFilesAndFolders(path: str, projectTree: ProjectTree):
    for relpath in projectTree.get_directories():
        if not make_dir_if_not_exists(path=path, fname=relpath):
            raise FileExistsError('Could not create (sub)folder \033[1m{}\033[0m'.format(relpath));
    for relfname in projectTree.get_files():
        if not make_file_if_not_exists(path=path, fname=relfname):
            raise FileExistsError('Could not create file \033[1m{}\033[0m'.format(relfname));
    return;

def createFileStamp(
    path: str,
    overwrite: bool,
    options: dict[str, Any]
):
    if os.path.exists(path) and not overwrite:
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
    path: str,
    overwrite: bool,
    options: dict[str, Any]
):
    if os.path.exists(path) and not overwrite:
        return;
    appconfig.setExportVars({});
    lines = [];
    for key, value in options.items():
        try:
            codedvalue = convert_to_python_string(value);
            appconfig.setExportVarsKeyValue(key=key, value=value, codedvalue=codedvalue);
            lines.append('<<< global set {key} = {value}; >>>'.format(key = key, value = codedvalue));
        except:
            continue;
    if os.path.isfile(path) and not overwrite:
        return;
    writeTextFile(path=path, lines=lines);
    return;

def createParameters(options: dict[str, Any]):
    appconfig.setExportVars({});
    lines = [];
    for key, value in options.items():
        try:
            codedvalue = convert_to_python_string(value);
            appconfig.setExportVarsKeyValue(key=key, value=value, codedvalue=codedvalue);
        except:
            continue;
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TERTIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def make_file_if_not_exists(path: str, fname: str) -> bool:
    fname_full = os.path.join(path, fname);
    try:
        if not os.path.isfile(fname_full):
            log_info('File \033[96;1m{}\033[0m will be created.'.format(fname));
            createFile(fname_full);
    except:
        pass;
    return os.path.isfile(fname_full);

def make_dir_if_not_exists(path: str, fname: str) -> bool:
    fname_full = os.path.join(path, fname);
    try:
        if not os.path.isdir(fname_full):
            log_info('Folder \033[96;1m{}\033[0m will be created.'.format(fname));
            createPath(path=fname_full);
    except:
        pass;
    return os.path.isdir(fname_full);
