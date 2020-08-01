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
from ..core.utils import Inf;
from ..core.utils import INFINITY;
from ..core.utils import parse_cli_args;
from ..core.utils import parse_type;
from .examples import Examples;
from .values import Value;
from .keys import Key;
from .validity import Validity;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BASIC_TYPES = ['boolean', 'bool', 'numeric', 'int', 'float', 'string' 'url', 'email'];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Argument
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Argument:
    key: Key = Key();
    required: bool = False;
    multiple_specified: bool = False;
    numberofarguments: List[Union[int, Inf]] = [1, 1];
    cli_type: str = '';
    value_type: Union[None, str, List[str]] = None;
    value: Value = Value();
    default: Union[None, str, bool, int, float] = None;
    default_description: Union[None, str] = None;
    description: str = r'—';
    examples: Examples = Examples();

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
        if isinstance(key, (str, list)):
            self.key = Key(key);
        if not cli_type is None:
            self.cli_type = cli_type;
        if not value_type is None:
            self.value_type = value_type;
        if not description is None:
            self.description = description;

        if self.takes_value:
            if not required is None:
                self.required = required;
            minimum = 1 if self.required else 0;
            self.numberofarguments = [minimum, 1];
            if not multiple is None:
                self.multiple_specified = True;
                self.numberofarguments = Argument.set_range(minimum, multiple);
        else:
            self.required = False;
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
            self.examples = Examples(*[example[_] for _ in example]);
        return;

    @property
    def takes_value(self) -> bool:
        return self.cli_type in ['key-value', 'key-space-value'];

    @property
    def state(self) -> List[Validity]:
        validities = [];
        if self.takes_value:
            [u, v] = self.numberofarguments;
            n = len(self.value);
            value_valid = self.value.valid;
            if n == 0 and u == 1:
                validities.append(Validity(kind='required'));
            elif n < u:
                validities.append(Validity(kind='min-args', expected=u, actual=n));
            if n > v:
                validities.append(Validity(kind='max-args', expected=v, actual=n));
            if not value_valid:
                validities.append(Validity(kind='value'));
        return validities;

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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Arguments
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Arguments:
    __arguments: Dict[str, Argument] = dict();
    __tokens: List[Tuple[str, bool]] = [];

    def __init__(self):
        return;

    def __iter__(self):
        for label in self.__arguments:
            yield label, self.__arguments[label];

    def __len__(self) -> int:
        return len(self.__arguments);

    def __str__(self):
        values = self.values;
        return str(dict(
            tokens=self.tokens,
            values={key: str(values[key]) for key in values},
        ));

    @property
    def tokens(self) -> List[str]:
        return [label for label, accept in self.__tokens if accept];

    @property
    def labels(self) -> List[str]:
        return [label for label in self.__arguments  if self.__arguments[label].takes_value];

    @property
    def values(self) -> Dict[str, Value]:
        return {label: self.__arguments[label].value for label in self.labels};

    @property
    def state(self) -> List[Tuple[str, List[Validity], Argument]]:
        return [(label, argument.state, argument) for label, argument in self.__iter__()];

    def add(self, label: str, argument: Argument):
        if label in self.__arguments:
            del self.__arguments[label];
        self.__arguments[label] = argument;

    def parse(self, *args: str):
        self.__tokens = [];
        tokens, kwargs, ksargs = parse_cli_args(*args, strict=True, ignorecase=True);
        for label, argument in self.__iter__():
            if argument.takes_value:
                valid, values = parse_one_kw(argument, kwargs, ksargs);
                value = Value(
                    default=argument.default,
                    values=values,
                    value=values[0] if len(values) > 0 else argument.default,
                    valid=valid
                );
                argument.value = value;
            else:
                value = parse_one_token(argument, tokens);
                self.__tokens.append((label, value));
        return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parse_one_token(argument: Argument, tokens: List[str]) -> bool:
    for key in argument.key:
        if key in tokens:
            return True;
    return False;

def parse_one_kw(argument: Argument, kwargs: Dict[str, List[str]], ksargs: Dict[str, List[str]]) -> Tuple[bool, list]:
    values = [];
    if argument.cli_type == 'key-value':
        for key in argument.key:
            if key in kwargs:
                values += kwargs[key];
    else:
        for key in argument.key:
            if key in ksargs:
                values += ksargs[key];
    # parse values to type, and only retain acceptable values:
    if argument.value_type is None:
        valid = True;
    else:
        values = [parse_type(val, argument.value_type) for val in values];
        valid = not(False in [accept for _, accept in values]);
        values = [val for val, accept in values if accept];
    return valid, values

def display_key(key: Key) -> str:
    return ' / '.join([ '\033[93m{}\033[0m'.format(x) for x in key]);

def display_value_type(value_type: Union[None, str, List[str]]) -> str:
    if value_type is None:
        return '';
    if isinstance(value_type, str):
        if value_type in BASIC_TYPES:
            return '<{}>'.format(value_type);
        return value_type;
    return ' | '.join([ display_value_type(x) for x in value_type]);

def display_command(typ: str, key: Key, value_type: Union[None, str, List[str]], required: bool) -> str:
    key_ = display_key(key);
    if typ in ['key-value', 'key-space-value']:
        sep = ' ' if typ == 'key-space-value' else '=';
        value_type_ = display_value_type(value_type);
        command = '{key}{sep}{value_type}'.format(key=key_, sep=sep, value_type=value_type_);
    else:
        command = key_;
    return command if required else '[ {} ]'.format(command);
