#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import src.paths;

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
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'step_create',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step create
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step_create(user_config: UserConfig):
    log_info('CREATION STAGE STARTED.');

    generate_tree(
        path = src.paths.wd,
        files = user_config.files,
        folders = user_config.folders,
    );

    if user_config.stamp is not None:
        create_file_stamp(
            path = user_config.stamp.file,
            overwrite = user_config.stamp.overwrite,
            options = user_config.stamp.options,
        );

    if user_config.parameters is not None:
        create_parameters(options=user_config.parameters.options);

    log_info('CREATION STAGE COMPLETE.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_tree(path: str, files: list[str], folders: dict[str, DataTypeFolder]):
    # create all files at current level:
    for name in files:
        log_info(f'File \033[96;1m{name}\033[0m will be created.');
        create_file_if_not_exists(path=os.path.join(path, name));
    # create all folders at current level:
    for name, object in folders.items():
        log_info(f'Directory \033[96;1m{name}\033[0m will be created.');
        create_dir_if_not_exists(path=os.path.join(path, name));
    # create recursively handle subfolders:
    for name, object in folders.items():
        generate_tree(path=os.path.join(path, name), files=object.files, folders=object.folders);
    return;

def create_file_stamp(
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
    write_text_file(path=path, lines=lines);
    return;

def create_parameters(options: dict[str, Any]):
    # config.set_export_vars({});
    # for key, value in options.items():
    #     try:
    #         codedvalue = convert_to_python_string(value);
    #         config.set_export_vars_key_value(key=key, value=value, codedvalue=codedvalue);
    #     except:
    #         continue;
    return;

# def create_file_parameters(
#     path: str,
#     overwrite: bool,
#     options: dict[str, Any]
# ):
#     if os.path.exists(path) and not overwrite:
#         return;
#     config.set_export_vars({});
#     lines = [];
#     for key, value in options.items():
#         try:
#             codedvalue = convert_to_python_string(value);
#             config.set_export_vars_key_value(key=key, value=value, codedvalue=codedvalue);
#             lines.append('<<< global set {key} = {value}; >>>'.format(key = key, value = codedvalue));
#         except:
#             continue;
#     if os.path.isfile(path) and not overwrite:
#         return;
#     write_text_file(path=path, lines=lines);
#     return;
