#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import re;
from typing import Any;
from typing import Union;

from ..__path__ import project_path;
from ..core.utils import len_pure;
from ..core.utils import pad_strings;
from ..core.config import Struct;
from ..core.logger import Logger;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BASIC_TYPES = ['boolean', 'bool', 'numeric', 'int', 'float', 'string' 'url', 'email'];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Help
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Help:
    __log: Logger;
    __struct: Struct;
    __version: Union[str, None] = None;

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
            self.__version = get_version();
        return self.__version;

    @property
    def log(self) -> Logger:
        return self.__log;

    @property
    def struct(self) -> Struct:
        return self.__struct;

    def console_help(self, part: str):
        self.log.plain('');
        self.console_print_title(part);
        self.log.plain('');
        self.console_print_command(part);
        self.log.plain('');
        self.console_print_arguments(part);
        self.log.plain('');
        self.console_print_examples(part);
        self.log.plain('');
        return;

    def console_print_title(self, part: str):
        author = self.struct.getValue('author');
        date = self.struct.getValue('date');
        site = self.struct.getValue('site');
        name = self.struct.getName('cli', part);
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
        command = self.struct.getValue('cli', part, 'command');
        self.log.plain('  \033[1;4;92mBasic command\033[0m:', '', sep='\n');
        self.log.plain('    \033[1;93m{}\033[0m \033[2m[+ arguments]\033[0m'.format(command));
        return;

    def console_print_arguments(self, part: str):
        arguments = self.struct.getValue('cli', part, 'arguments', default={});
        self.log.plain('  \033[1;4;92mArguments\033[0m:');
        for key in arguments:
            options = Struct.get_value(arguments, key);
            self.log.plain('');
            self.console_print_argument(options);
        return;

    def console_print_argument(self, options: Any):
        typ = Struct.get_value(options, 'type');
        key = Struct.get_value(options, 'key');
        required = Struct.get_value(options, 'required');
        description = Struct.get_value(options, 'description');
        value = Struct.get_value(options, 'value');
        default = Struct.get_value(options, 'default');
        if typ in ['key-value', 'key-space-value']:
            value_type = value;
            if value in BASIC_TYPES:
                value_type = '<{}>'.format(value);
            sep = ' ' if typ == 'key-space-value' else '=';
            command = '\033[1;93m{key}\033[0m{sep}{value}'.format(key=key, sep=sep, value=value_type);
        # elif typ == 'key':
        else:
            command = '\033[1;93m{}\033[0m'.format(key);
        command = command if required else '[ {} ]'.format(command);
        self.log.plain('    {}'.format(command));
        if typ == 'key-value' and not default is None:
            self.log.plain('      \033[3;2mdefault\033[0m\033[2m: {}\033[0m'.format(default));
            pass;
        self.log.plain('      \033[3mdescription\033[0m: {}'.format(description));
        return;

    def console_print_examples(self, part: str):
        arguments = self.struct.getValue('cli', part, 'arguments', default={});
        self.log.plain('  \033[1;4;92mExamples\033[0m:');
        for key in arguments:
            examples = Struct.get_value(arguments, key, 'example', default={});
            for key_ in examples:
                options = Struct.get_value(examples, key_);
                self.log.plain('');
                self.console_print_example(options);
        return;

    def console_print_example(self, options: Any):
        command = Struct.get_value(options, 'command');
        result = Struct.get_value(options, 'result');
        self.log.plain('    \033[3mcommand\033[0m: \033[96m{}\033[0m'.format(command));
        self.log.plain('    \033[3mresult\033[0m: {}'.format(result));
        return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_version() -> str:
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
