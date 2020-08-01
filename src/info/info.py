#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import re;
from typing import Union;

from ..__path__ import project_path;
from ..core.config import Struct;
from ..core.utils import INFINITY, static;
from ..core.utils import len_pure;
from ..core.utils import pad_strings;
from ..core.logger import Logger;
from .arguments import Argument;
from .arguments import Arguments;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Info
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Info:
    __log: Logger;
    __struct: Struct;
    __version: Union[str, None] = None;
    __arguments: Arguments;

    def __init__(self, log: Logger):
        self.__initialise(log);
        return;

    def __initialise(self, log: Logger):
        self.__log = log;
        self.__struct = Struct(fname=os.path.join('docs', 'help.yml'));
        return;

    @property
    def version(self) -> Union[str, None]:
        if self.__version is None:
            self.__version = Info.version;
        return self.__version;

    @property
    def log(self) -> Logger:
        return self.__log;

    @property
    def struct(self) -> Struct:
        return self.__struct;

    @property
    def arguments(self) -> Arguments:
        return self.__arguments;

    @static
    def version(cls) -> str:
        version = None;
        try:
            with open(project_path('VERSION')) as fp:
                for line in fp.readlines():
                    line = re.sub(r'^[\s\n\r]+|[\s\n\r]+$', r'', line);
                    if not re.match(r'^\d+\.\d+\.\d+$', line):
                        continue;
                    version = line;
                    break;
            if version is None:
                raise ValueError('Value in VERSION file is invalid!');
        except:
            raise FileNotFoundError('VERSION file missing in the distribution folder or could not be opened in read mode!');
        return version;

    def get_attributes(self, *keys: str, default=None):
        return self.struct.getValue(*keys, default=default);

    def get_name(self, *keys: str):
        return self.struct.getName(*keys);

    def parse_arguments(self, part):
        self.__arguments = Arguments();
        arguments = self.get_attributes('cli', part, 'arguments', default={});
        for key in arguments:
            argument = Argument(**(arguments[key] or {}));
            self.__arguments.add(key, argument);
        return self.__arguments;

    def console_help(self, part: str):
        self.log.plain('');
        self.console_print_title(part);
        self.log.plain('');
        self.console_print_command(part);
        self.log.plain('');
        self.console_print_arguments();
        self.log.plain('');
        self.console_print_examples();
        self.log.plain('');
        return;

    def console_print_title(self, part: str):
        author = self.get_attributes('author');
        date = self.get_attributes('date');
        site = self.get_attributes('site');
        name = self.get_name('cli', part);
        version = self.version or '???';
        title = pad_strings(
            '',
            'Usage of \033[92m{name}\033[0m v\033[1m{version}\033[0m'.format(name=name, version=version),
            '   ~~~~ {site}/\033[1;91m{author}\033[0m, {date}'.format(site=site, author=author, date=date),
            '',
        sep=' ');
        title = [ ' |    ' + line + '    |' for line in title];
        n = len_pure(title[0]);
        bar = ' ' + '-'*(n - 1);
        title = [bar] + title + [bar];
        self.log.plain(*title, sep='\n');
        return;

    def console_print_command(self, part: str):
        command = self.get_attributes('cli', part, 'command');
        self.log.plain('  \033[1;4;92mBasic command\033[0m:', '', sep='\n');
        self.log.plain('    \033[1;93m{}\033[0m \033[2m[+ arguments]\033[0m'.format(command));
        return;

    def console_print_arguments(self):
        self.log.plain('  \033[1;4;92mArguments\033[0m:');
        for _, argument in self.arguments:
            self.log.plain('');

            ## display command:
            self.log.plain('    {}'.format(Argument.display_command(argument.cli_type, argument.key, argument.value_type, argument.required)));

            ## display information re. multiple argument, provided the 'multiple:' argument has been specified:
            if argument.multiple_specified:
                [u, v] = argument.numberofarguments;
                if u == 1 and v == INFINITY:
                    self.log.plain('      \033[3;2mmultiple arguments\033[0m: allowed.'.format());
                elif u > 1 and v == INFINITY:
                    self.log.plain('      \033[3;2mmultiple arguments\033[0m: at least {} arguments required.'.format(u));
                elif u == 1 and v > 1:
                    self.log.plain('      \033[3;2mmultiple arguments\033[0m: at most {} arguments allowed.'.format(v));
                elif u == 1 and v == 1:
                    self.log.plain('      \033[3;2mmultiple arguments\033[0m: not allowed.'.format());
                else:
                    self.log.plain('      \033[3;2mmultiple arguments\033[0m: between {} and {} arguments required.'.format(u, v));

            ## show default value, if provided:
            if argument.cli_type in ['key-value', 'key-space-value']:
                if not argument.default is None:
                    self.log.plain('      \033[3;2mdefault\033[0m\033[2m: {}\033[0m'.format(argument.default));
                elif not argument.default_description is None:
                    self.log.plain('      \033[3;2mdefault\033[0m\033[2m: {}\033[0m'.format(argument.default_description));

            ## show description:
            self.log.plain('      \033[3mdescription\033[0m: {}'.format(argument.description));
        return;

    def console_print_examples(self):
        self.log.plain('  \033[1;4;92mExamples\033[0m:');
        for _, argument in self.arguments:
            for example in argument.examples:
                self.log.plain('');
                self.log.plain('    \033[3mcommand\033[0m: \033[96m{}\033[0m'.format(example.command));
                self.log.plain('    \033[3mresult\033[0m: {}'.format(example.result));
        return;
