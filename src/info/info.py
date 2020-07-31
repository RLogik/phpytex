#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import re;
from typing import Any;
from typing import Dict;
from typing import List;
from typing import Union;
from typing import Tuple;

from ..__path__ import project_path;
from ..core.config import Struct;
from ..core.utils import static;
from ..core.utils import Inf;
from ..core.utils import INFINITY;
from ..core.utils import len_pure;
from ..core.utils import pad_strings;
from ..core.utils import parse_type;
from ..core.logger import Logger;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Example
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Example
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Example:
    command: str = '';
    result: str = '';

    def __init__(self, command = None, result = None, **kwargs):
        if not command is None:
            self.command = command;
        if not result is None:
            self.result = result;
        return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Argument
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Argument:
    key: Union[str, List[str]];
    required: bool = False;
    multiple_specified: bool = False;
    multiple: List[Union[int, Inf]] = [1, 1];
    cli_type: str = '';
    value_type: Union[None, str, List[str]] = None;
    default: Union[None, str, bool, int, float] = None;
    default_description: Union[None, str] = None;
    description: str = r'—';
    examples: List[Example] = [];

    def __init__(
        self,
        key = None,
        required = None,
        multiple = None,
        cli_type = None,
        value_type = None,
        default = None,
        description = None,
        example: Dict[str, Dict[str, str]] = None,
        **kwargs
    ):
        if not key is None:
            self.key = key;
        if not required is None:
            self.required = required;
        if not value_type is None:
            self.value_type = value_type;
        if not description is None:
            self.description = description;
        if not cli_type is None:
            self.cli_type = cli_type;
        if self.takes_value():
            minimum = 1 if self.required else 0;
            self.multiple[0] = minimum;
            if not multiple is None:
                self.multiple_specified = True;
                self.multiple = Argument.set_range(minimum, multiple);
        else:
            self.multiple = [0, 0];

        default_description = None;
        if isinstance(default, dict):
            default_description = Struct.get_value(default, 'description', default=None);
            default = Struct.get_value(default, 'value', default=None);
        if not default is None:
            self.default = default;
        if not default_description is None:
            self.default_description = default_description;

        if not example is None:
            self.examples = [Example(**example[key]) for key in example];
        return;

    @static
    def BASIC_TYPES(cls) -> List[str]:
        return ['boolean', 'bool', 'numeric', 'int', 'float', 'string' 'url', 'email'];

    @classmethod
    def set_range(cls, MIN: int, _interval: Union[bool, List[Union[int, float]]]) -> List[Union[int, Inf]]:
        if isinstance(_interval, bool):
            if _interval:
                return [MIN, INFINITY];
            else:
                return [MIN, MIN];
        else:
            if len(_interval) == 0:
                u = MIN;
                v = MIN;
            elif len(_interval) < 2:
                u = _interval[0];
                v = u;
            else:
                [u, v] = _interval[:2];
            u = int(u) if u < float('inf') else INFINITY;
            v = int(v) if v < float('inf') else INFINITY;
            return [u, v];

    @classmethod
    def display_key(cls, key: Union[str, List[str]]) -> str:
        if isinstance(key, str):
            return '\033[93m{}\033[0m'.format(key);
        return ' / '.join([ cls.display_key(x) for x in key]);

    @classmethod
    def display_value_type(cls, value_type: Union[None, str, List[str]]) -> str:
        if value_type is None:
            return '';
        if isinstance(value_type, str):
            if value_type in cls.BASIC_TYPES:
                return '<{}>'.format(value_type);
            return value_type;
        return ' | '.join([ cls.display_value_type(x) for x in value_type]);

    @classmethod
    def display_command(cls, typ: str, key: Union[str, List[str]], value_type: Union[None, str, List[str]], required: bool) -> str:
        key_ = cls.display_key(key);
        if typ in ['key-value', 'key-space-value']:
            sep = ' ' if typ == 'key-space-value' else '=';
            value_type_ = cls.display_value_type(value_type);
            command = '{key}{sep}{value_type}'.format(key=key_, sep=sep, value_type=value_type_);
        else:
            command = key_;
        return command if required else '[ {} ]'.format(command);

    def takes_value(self) -> bool:
        return self.cli_type in ['key-value', 'key-space-value'];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Values
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Value:
    value: Union[None, bool, str, int, float, List[Union[None, bool, str, int, float]]];
    value_one: Union[None, bool, str, int, float];
    default: Union[None, bool, str, int, float];

    def __init__(self, value=None, value_one=None, default=None, **kwargs):
        self.value = value;
        self.value_one = value_one;
        self.default = default;

    def __str__(self):
        return str(self.value);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Arguments
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Arguments:
    __arguments: Dict[str, Argument] = dict();
    __tokens: List[Tuple[str, bool]] = [];
    __kwargs: Dict[str, Value] = dict();

    def __init__(self):
        return;

    def __iter__(self):
        for label in self.__arguments:
            yield label, self.__arguments[label];

    def __str__(self):
        kwvalues = self.kwvalues;
        return str(dict(
            tokens=str(self.tokens),
            kwvalues=str({key: str(kwvalues[key]) for key in kwvalues}),
        ));

    def add(self, label: str, argument: Argument):
        if label in self.__arguments:
            del self.__arguments[label];
        self.__arguments[label] = argument;

    @property
    def tokens(self) -> List[str]:
        return [label for label, accept in self.__tokens if accept];

    @property
    def kwvalues(self) -> Dict[str, Value]:
        return self.__kwargs;

    def parse(self, *args: str):
        for label in self.__arguments:
            argument = self.__arguments[label];
            value = Arguments.parse_one(argument, *args);
            if isinstance(value, list):
                self.__kwargs[label] = Value(
                    default=argument.default,
                    value=value,
                    value_one=value[0] if len(value) > 0 else argument.default,
                );
            else:
                self.__tokens.append((label, value));
        return;

    @classmethod
    def parse_one(cls, argument: Argument, *args: str) -> Union[bool, list]:
        keys = argument.key;
        if not isinstance(keys, list):
            keys = [keys];
        if argument.takes_value():
            values = [];
            if argument.cli_type == 'key-value':
                for arg in args:
                    m = re.match(r'^(.*?)\=(.*)$', arg);
                    if not m:
                        continue;
                    _key = m.group(1);
                    if _key in keys:
                        value = m.group(2);
                        values.append(value);
            else:
                n = len(args);
                values = [args[k+1] for k in range(n-1) if args[k] in keys];

            # parse values to type, and only retain acceptable values:
            if not argument.value_type is None:
                values = [parse_type(val, argument.value_type) for val in values];
                values = [val for val, accept in values if accept];

            [u, v] = argument.multiple;
            # truncate arguments, if too many are given:
            if len(values) > v and isinstance(v, int):
                values = values[:v];
            # append arguments, if too few are given:
            if len(values) < u and isinstance(u, int):
                default = argument.default;
                n = u-len(values);
                values += [default for _ in range(n)];
            return values
        else:
            for key in keys:
                if key in args:
                    return True;
            return False;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Help
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Help:
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
            self.__version = get_version();
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

    def get_cli_structure(self, part):
        self.__arguments = Arguments();
        arguments = self.struct.getValue('cli', part, 'arguments', default={});
        for key in arguments:
            argument = Argument(**(arguments[key] or {}));
            self.__arguments.add(key, argument);
        return self.__arguments;

    def console_help(self, part: str):
        self.get_cli_structure(part);
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

    def console_print_arguments(self):
        self.log.plain('  \033[1;4;92mArguments\033[0m:');
        for _, argument in self.arguments:
            self.log.plain('');

            ## display command:
            self.log.plain('    {}'.format(Argument.display_command(argument.cli_type, argument.key, argument.value_type, argument.required)));

            ## display information re. multiple argument, provided the 'multiple:' argument has been specified:
            if argument.multiple_specified:
                [u, v] = argument.multiple;
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
