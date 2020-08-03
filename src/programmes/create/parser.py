#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
from typing import List;
from typing import Tuple;
from gitignore_parser import parse_gitignore;

from .make import Make;
from .make import CompilerConfig;
from ...values.struct import Struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def extract_specs(recursive: bool, config: Struct, path: str) -> List[Tuple[str, Struct]]:
    ext_create = config.getValue('file-extension-create');
    ext_ignore = config.getValue('file-extension-create-ignore');

    match_ignore = None;
    # extract ignore file (if one exists)
    for fname in os.listdir(path):
        if fname.endswith(ext_ignore):
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
        files = [fname for fname in files if fname.endswith(ext_create)];
        if len(files) == 0:
            if subpath == path:
                raise FileNotFoundError('No file with extension \'{}\' could be found in the project directory!'.format(ext_create));
        else:
            fname = files[0];
            # extract instruction for structure from yml file:
            config = Struct(fname=os.path.join(subpath, fname));
            # process ignore instruction, except if in root:
            force_ignore = not(subpath == path) and config.getValue('ignore', default=False);
            if force_ignore is False:
                specifications.append([subpath, config, True]);
            elif force_ignore is True:
                pass;
            elif force_ignore in ['backwards', 'backward']:
                ignore.append(subpath);
            elif force_ignore in ['backwards-strict', 'backward-strict', 'strict']:
                specifications.append([subpath, config, True]);
                ignore.append(subpath);
        if not recursive and (subpath == path):
            break;

    # now filter out all paths, which the yaml files tell to ignore:
    for subpath in ignore:
        for k, [_subpath, config, accept] in enumerate(specifications):
            if not accept and not (_subpath == subpath) and _subpath.startswith(subpath):
                specifications[k][2] = False;

    return [(subpath, config) for subpath, config, accept in specifications if accept];

def process_specs(make: Make, path: str, config: Struct, is_root: bool):
    # create files:
    files = config.getValue('files', default=dict());
    for _, fname, _ in Struct.get_parts(files):
        make.file_if_not_exists(fname, path);
        pass;

    # create folders recursively:
    folders = config.getValue('components', default=dict());
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

    # ONLY if at root level: create root and output files, compile script:
    # create root file
    file_root = config.getValue('compile', 'options', 'root', default='root.tex');
    make.file_if_not_exists(file_root, path);

    # create output file
    file_output = config.getValue('compile', 'options', 'output', default=None);
    if isinstance(file_output, str):
        make.file_if_not_exists(file_output, path);

    # if provided, create and fill start script:
    options = config.getValue('compile', 'options', default={});
    file_runscript = config.getValue('compile', 'file');
    file_output = Struct.get_value(options, 'output');
    overwrite = config.getValue('compile', 'overwrite', default=False);
    if isinstance(file_runscript, str) and isinstance(file_output, str):
        fexists = make.file_if_not_exists(file_runscript, path);
        if not fexists or overwrite:
            compiler_config = CompilerConfig(
                root          = file_root,
                stamp         = file_stamp,
                output        = file_output,
                debug         = Struct.get_value(options, 'debug'),
                compile_latex = Struct.get_value(options, 'compile-latex'),
                insert_bib    = Struct.get_value(options, 'insert-bib'),
                comments      = Struct.get_value(options, 'latex-comments'),
                show_tree     = Struct.get_value(options, 'show-tree'),
                tabs          = Struct.get_value(options, 'tabs'),
                spaces        = Struct.get_value(options, 'spaces'),
                max_length    = Struct.get_value(options, 'max-length'),
                seed          = Struct.get_value(options, 'seed')
            );
            lines = make.start_script(
                root          = compiler_config.root,
                stamp         = compiler_config.stamp,
                output        = compiler_config.output,
                debug         = compiler_config.debug,
                compile_latex = compiler_config.compile_latex,
                insert_bib    = compiler_config.insert_bib,
                comments      = compiler_config.comments,
                show_tree     = compiler_config.show_tree,
                tabs          = compiler_config.tabs,
                spaces        = compiler_config.spaces,
                max_length    = compiler_config.max_length,
                seed          = compiler_config.seed
            );
            make.write_to_file(*lines, fname=file_runscript, path=path);
    return;