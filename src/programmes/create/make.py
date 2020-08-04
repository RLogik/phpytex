#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
from subprocess import Popen;
from typing import Any;
from typing import List;
from typing import Tuple;

from ...core.logger import LoggerService;
from ...info.arguments import Arguments;
from ...values.keys import Key;
from ...values.struct import Struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Auxilary class: CompilerConfig
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompilerConfig:
    arguments: Arguments;
    def __init__(self, arguments: Arguments):
        self.arguments = arguments;
        return;

    def parse(self, **spec) -> List[Tuple[str, Key, Any]]:
        results = [];
        # compare arguments obtained from .phpycreate.yml (spec)
        # with argument structure obtained from the configuration (self.arguments)
        for label, argument in self.arguments:
            # if a key has been set, then add it, even if the argument is invalid.
            if label in spec:
                value = spec[label];
            # if a key has not been set, then add the default value, provided the argument is required.
            else:
                value = argument.defaultValue;
                if not argument.required:
                    continue;

            # under no circumstances add a None/null value.
            if value is None:
                continue;

            key = argument.key;
            cli_type = argument.cli_type;
            # if the cli-type is key, and the value is not true, then there is no argument to add.
            if cli_type == 'key' and not (value is True):
                continue;

            # otherwise we add the cli-type, key, and value:
            results.append((cli_type, key, value));

        return results;

    def create_command(self, basiccommand: str, **spec) -> str:
        results = self.parse(**spec);
        parts = [];
        for cli_type, key, value in results:
            if cli_type == 'key':
                parts += ['{key}'.format(key=key)];
            elif cli_type == 'key-value':
                parts += ['{key}={value}'.format(key=key, value=value)];
            elif cli_type == 'key-space-value':
                parts += ['{key} {value}'.format(key=key, value=value)];
        return '{basic} {parts}'.format(basic=basiccommand, parts=' '.join(parts));

    # @transfer
    # class CompilerConfig(Configurable):
    #     _DEFAULT = dict(
    #         input         = ValueType(str, None),
    #         stamp         = ValueType(str, None),
    #         output        = ValueType(str, None),
    #         debug         = ValueType(bool, False),
    #         compile_latex = ValueType(bool, True),
    #         insert_bib    = ValueType(bool, False),
    #         comments      = ValueType(['partial', 'on', 'off', bool], 'partial'),
    #         show_tree     = ValueType(bool, True),
    #         tabs          = ValueType(bool, False),
    #         spaces        = ValueType(int, 4),
    #         max_length    = ValueType(int, 10000),
    #         seed          = ValueType(int, None),
    #     );

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
