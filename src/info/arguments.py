#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Dict;
from typing import List;
from typing import Union;
from typing import Tuple;

from ..core.config import Struct;
from ..core.utils import static;
from ..core.utils import Inf;
from ..core.utils import INFINITY;
from ..core.utils import parse_cli_args;
from ..core.utils import parse_type;
from .examples import Example;
from .values import Value;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Argument
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Argument:
    key: Union[str, List[str]];
    required: bool = False;
    multiple_specified: bool = False;
    numberofarguments: List[Union[int, Inf]] = [1, 1];
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
            self.numberofarguments[0] = minimum;
            if not multiple is None:
                self.multiple_specified = True;
                self.numberofarguments = Argument.set_range(minimum, multiple);
        else:
            self.numberofarguments = [0, 0];

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
# Class: Arguments
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Arguments:
    __arguments: Dict[str, Argument] = dict();
    __tokens: List[Tuple[str, bool]] = [];
    __labelled_values: Dict[str, Value] = dict();

    def __init__(self):
        return;

    def __iter__(self):
        for label in self.__arguments:
            yield label, self.__arguments[label];

    def __str__(self):
        values = self.values;
        return str(dict(
            tokens=self.tokens,
            values={key: str(values[key]) for key in values},
        ));

    def add(self, label: str, argument: Argument):
        if label in self.__arguments:
            del self.__arguments[label];
        self.__arguments[label] = argument;

    @property
    def tokens(self) -> List[str]:
        return [label for label, accept in self.__tokens if accept];

    @property
    def values(self) -> Dict[str, Value]:
        return self.__labelled_values;

    def parse(self, *args: str):
        self.__tokens = [];
        self.__labelled_values = dict();
        tokens, kwargs, ksargs = parse_cli_args(*args, strict=True, ignorecase=True);
        for label in self.__arguments:
            argument = self.__arguments[label];
            values = Arguments.parse_one(argument, tokens, kwargs, ksargs);
            if isinstance(values, list):
                self.__labelled_values[label] = Value(
                    default=argument.default,
                    values=values,
                    value=values[0] if len(values) > 0 else argument.default,
                );
            else:
                value = values;
                self.__tokens.append((label, value));
        return;

    @classmethod
    def parse_one(cls,
        argument: Argument,
        tokens: List[str],
        kwargs: Dict[str, List[str]],
        ksargs: Dict[str, List[str]]
    ) -> Union[bool, list]:
        keys = argument.key;
        if not isinstance(keys, list):
            keys = [keys];
        if argument.takes_value():
            values = [];
            for key in keys:
                if key in kwargs:
                    if argument.cli_type == 'key-value':
                        values += kwargs[key];
                    else:
                        values += ksargs[key];
            # parse values to type, and only retain acceptable values:
            if not argument.value_type is None:
                values = [parse_type(val, argument.value_type) for val in values];
                values = [val for val, accept in values if accept];

            [u, v] = argument.numberofarguments;
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
                if key in tokens:
                    return True;
            return False;
