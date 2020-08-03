#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from subprocess import Popen
from typing import List, Union;

from ...core.logger import LoggerService;
from ...values.configurable import Configurable;
from ...values.configurable import transfer;
from ...values.struct import Struct;
from ...values.valuetypes import ValueType

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Auxilary class: CompilerConfig
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@transfer
class CompilerConfig(Configurable):
    _DEFAULT = dict(
        root          = ValueType(str, None),
        stamp         = ValueType(str, None),
        output        = ValueType(str, None),
        debug         = ValueType(bool, False),
        compile_latex = ValueType(bool, True),
        insert_bib    = ValueType(bool, False),
        comments      = ValueType(['partial', 'on', 'off', bool], 'partial'),
        show_tree     = ValueType(bool, True),
        tabs          = ValueType(bool, False),
        spaces        = ValueType(int, 4),
        max_length    = ValueType(int, 10000),
        seed          = ValueType(int, None),
    );

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Make
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Make:
    log: LoggerService;
    wd: str;

    def __init__(self, log: LoggerService, wd: str):
        self.log = log;
        self.wd = wd;

    def file_if_not_exists(self, fname: str, path: str = None) -> bool:
        path = path or self.wd;
        fexists = os.path.isfile(os.path.join(path, fname));
        if not fexists:
            self.log.info('  \033[96mcreating file\033[0m \033[1m{}\033[0m'.format(fname));
            Popen(['touch', fname], cwd=path).wait();
        return fexists;

    def dir_if_not_exists(self, dir_name: str, path: str = None) -> bool:
        path = path or self.wd;
        fexists = os.path.isdir(os.path.join(path, dir_name));
        if not fexists:
            self.log.info('  \033[96mcreating folder\033[0m \033[1m{}\033[0m'.format(dir_name));
            Popen(['mkdir', '-p', dir_name], cwd=path).wait();
        return fexists;

    def write_to_file(self, *lines: str, fname: str, path: str = None):
        fname_full = fname;
        try:
            path = path or self.wd;
            fname_full = os.path.join(path, fname);
            self.log.info('  \033[96mwriting header contents to\033[0m \033[1m{}\033[0m'.format(fname));
            with open(fname_full, 'w') as fp:
                for line in lines:
                    fp.write(line + '\n');
        except:
            self.log.warning('!! Could not write to file `\033[1m{}\033[0m`. !! Check user permissions. Ensure that the file has not been deleted by another process.'.format(fname_full));
        return;

    def stamp(self, spec: dict) -> List[str]:
        lines = [];
        border = r'%% ' + '*'*80;

        max_tag_length = max([0] + [len(key) for key in spec]);
        for key in spec:
            value = spec[key];
            tag = key.upper();
            line = r'%% ' + tag + r':';
            if isinstance(value, list):
                indent = '\n' + r'%% ' + ' '*4;
                line += indent.join([''] + [u for u in value if isinstance(u, str)]);
            elif isinstance(value, (str, int, float, bool)):
                line += ' '*(1 + max_tag_length - len(tag)) + str(value);
            else:
                line += ' '*(1 + max_tag_length - len(tag)) + r'—';
            lines.append(line);
        if len(lines) > 0:
            lines = [border] + lines + [border];

        return lines;

    def start_script(self,
        root,
        stamp,
        output,
        debug,
        compile_latex,
        insert_bib,
        comments,
        show_tree,
        tabs,
        spaces,
        max_length,
        seed
    ) -> List[str]:

        lines = [];
        lines.append(r'#! /bin/bash');
        lines.append('');

        # CREATE PHPYTEX COMMAND:
        command = ['phpytex'];

        ################################################################
        ## FILES
        command += ['-i', root];
        # add stamp file?
        if isinstance(stamp, str):
            command += ['--stamp', stamp];
        command += ['-o', output];
        ################################################################

        ################################################################
        ## DEBUGGING, COMPILATION
        # debug? compile latex?
        if debug:
            command += ['--debug'];
        else:
            if compile_latex:
                command += ['--compile-latex=false'];
            else:
                command += ['--compile-latex=true'];
        ################################################################

        ################################################################
        # insert .bib contents into output file?
        if insert_bib:
            command += ['--insert-bib'];
        ################################################################

        ################################################################
        ## COMMENTS
        # handling of LaTeX comments:
        if comments in [True, 'on']:
            command += ['--comments=true'];
        elif comments in [False, 'off']:
            command += ['--comments=false'];
        else: # if latex_comment == 'partial'
            command += ['--comments=partial'];
        # show tree structure in output?
        command += ['--show-tree={}'.format(show_tree)];
        ################################################################

        ################################################################
        ## SPACING, LENGTH
        # add max length?
        if max_length > 0:
            command += ['--max-length', str(max_length)];
        # tabs or spaces
        if tabs:
            command += ['--tabs'];
        else:
            command += ['--spaces={}'.format(spaces)];
        lines.append(' '.join(command) + ';');
        ################################################################

        ################################################################
        ## RANDOM SEED
        # add seed?
        if isinstance(seed, int):
            command += ['--seed=', str(seed)];
        ################################################################

        return lines;

    def create_folders(self, dir_name: str, spec: dict, path: str):
        subpath = os.path.join(path, dir_name);

        # potentially add an index file:
        add_index = Struct.get_value(spec, 'add-index', default=True);
        if add_index:
            fname = 'index.tex';
            self.file_if_not_exists(fname, subpath);

        # add any files demanded:
        files = Struct.get_value(spec, 'files', default={});
        for _, fname, _ in Struct.get_parts(files):
            self.file_if_not_exists(fname, subpath);

        # add any subfolders demanded:
        folders = Struct.get_value(spec, 'components', default={});
        for _, dir_name_, struct_ in Struct.get_parts(folders):
            self.dir_if_not_exists(dir_name_, subpath);
            self.create_folders(dir_name_, struct_ or {}, subpath);
        return;
