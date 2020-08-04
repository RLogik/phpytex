#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import re
from typing import List;
from typing import Tuple;
from gitignore_parser import parse_gitignore;

from .make import Make;
from .make import CompilerConfig;
from ...core.utils import to_cli_key;
from ...values.struct import Struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def extract_specs(recursive: bool, config: Struct, path: str) -> List[Tuple[str, Struct]]:
    pattern_create = config.getValue('file-pattern-create', default=None);
    regex_create = re.compile(pattern_create);
    pattern_ignore = config.getValue('file-pattern-create-ignore', default=None);
    regex_ignore = re.compile(pattern_ignore);

    match_ignore = None;
    # extract ignore file (if one exists)
    for fname in os.listdir(path):
        if regex_ignore.match(fname):
            match_ignore = parse_gitignore(fname, base_dir=path);
            break;

    specifications = [];
    ignore = [];

    # first extract all phycreate yml files.
    for subpath, _, files in os.walk(path):
        # subpath is an absolute path.
        # files is a list of files in the path.
        if not recursive and not (subpath == path):
            continue;
        if not match_ignore is None and match_ignore(subpath):
            continue;
        files = [fname for fname in files if regex_create.match(fname)];
        if len(files) == 0:
            if subpath == path:
                raise FileNotFoundError('No file matching the pattern \'{}\' could be found in the project directory!'.format(pattern_create));
        else:
            fname = files[0];
            # extract instruction for structure from yml file:
            config = Struct(fname=os.path.join(subpath, fname));
            # process ignore-forwards instruction:
            _ignore_forwards = config.getValue('ignore-forwards', default=False);
            # process ignore instruction:
            _ignore = config.getValue('ignore', default=not(subpath == path) and _ignore_forwards);
            if not _ignore:
                specifications.append([subpath, config, True]);
            if _ignore_forwards:
                ignore.append(subpath);
        if not recursive and (subpath == path):
            break;

    # now filter out all paths, which the yaml files tell to ignore:
    for subpath in ignore:
        for k, [_subpath, config, accept] in enumerate(specifications):
            if not accept and not (_subpath == subpath) and _subpath.startswith(subpath):
                specifications[k][2] = False;

    return [(subpath, config) for subpath, config, accept in specifications if accept];

def process_specs(make: Make, basiccommand: str, compilerConfig: CompilerConfig, path: str, config: Struct, is_root: bool):
    # create files:
    files = config.getValue('files', default=dict());
    for _, fname, _ in Struct.get_parts(files):
        make.file_if_not_exists(fname, path);
        pass;

    # create folders recursively:
    folders = config.getValue('folders', default=dict());
    for _, dir_name, struct_ in Struct.get_parts(folders):
        make.dir_if_not_exists(dir_name, path);
        make.create_folders(dir_name, struct_ or {}, path=path);

    # if the instructions exist, create and fill the stamp file:
    file_stamp = config.getValue('stamp', 'file');
    if isinstance(file_stamp, str):
        fexists = make.file_if_not_exists(file_stamp, path);
        overwrite = config.getValue('stamp', 'overwrite', default=False);
        if not fexists or overwrite:
            lines = make.stamp(config.getValue('stamp', 'options', default=dict()));
            make.write_to_file(*lines, fname=file_stamp, path=path);
            pass;

    if not is_root:
        return;

    # ONLY if at root level: create and fill compile script:
    file_runscript = config.getValue('transpile', 'file');
    overwrite = config.getValue('transpile', 'overwrite', default=False);
    options = config.getValue('transpile', 'options', default={});
    if isinstance(file_runscript, str):
        fexists = make.file_if_not_exists(file_runscript, path);
        if not fexists or overwrite:
            cmd = compilerConfig.create_command(
                basiccommand,
                # need to do this to allow e.g. labels like 'show_tree' to be treated as 'show-tree':
                **{to_cli_key(label): options[label] for label in options}
            );
            make.write_to_file(*[r'#! /bin/bash', '', cmd], fname=file_runscript, path=path);
    return;
