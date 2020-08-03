#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
from typing import Any;
from typing import Dict;
from typing import List;
from typing import Union;
from typing import Tuple;

from ..core.utils import Inf;
from ..core.utils import INFINITY;
from ..core.parse import FlatType;
from ..core.parse import parse_type;
from ..core.parse import string_to_type;
from ..core.parse import type_to_string;
from ..values.struct import Struct;
from .examples import Examples;
from ..values.valuetypes import MultiValueType;
from ..values.keys import Key;
from ..values.validity import Validity;


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Argument
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Argument:
    key: Key = Key();
    required: bool = False;
    multiple_specified: bool = False;
    numberofarguments: List[Union[int, Inf]] = [1, 1];
    cli_type: str = '';
    value_type: FlatType;
    multivalue: MultiValueType = MultiValueType();
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
        # key
        if isinstance(key, (str, list)):
            self.key = Key(key);
        if not cli_type is None:
            self.cli_type = cli_type;

        # value and default values
        self.value_type = string_to_type(value_type);
        default_description = None;
        if isinstance(default, dict):
            default_description = Struct.get_value(default, 'description', default=None);
            default = Struct.get_value(default, 'value', default=None);
        if not default is None:
            self.default = default;
        if not default_description is None:
            self.default_description = default_description;
        self.multivalue = MultiValueType(values=[], default=self.default, valuetype=self.value_type);

        # multiplicity of arguments
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

        # descriptions and examples
        if not description is None:
            self.description = description;
        if not example is None:
            self.examples = Examples(*[example[_] for _ in example]);
        return;

    @property
    def takes_value(self) -> bool:
        return self.cli_type in ['key-value', 'key-space-value'];

    @property
    def value(self):
        return self.multivalue.value;

    @property
    def values(self):
        return self.multivalue.values;

    @property
    def state(self) -> List[Validity]:
        validities = [];
        if self.takes_value:
            [u, v] = self.numberofarguments;
            n = len(self.multivalue);
            value_valid = self.multivalue.valid;
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
# Class: ArgumentValues
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ArgumentValues:
    __multivalues: List[Tuple[str, MultiValueType]];

    def __init__(self, **kwargs):
        self.__multivalues = [];
        for label in kwargs:
            item = kwargs[label];
            if isinstance(item, MultiValueType):
                self.__multivalues.append((label, item));
        return;

    def __iter__(self):
        for label, item in self.__multivalues:
            yield label, item;

    def __str__(self):
        return str({label: str(item) for label, item in self.__iter__()});

    def getMultiValue(self, label: str) -> MultiValueType:
        for _label, item in self.__iter__():
            if _label == label:
                return item;
        raise ValueError('No key {} was found'.format(label));

    def getValue(self, label: str) -> Any:
        return self.getMultiValue(label).value;

    def getValues(self, label: str) -> Any:
        return self.getMultiValue(label).values;

    def getValueAsBoolean(self, label: str) -> bool:
        return bool(self.getValue(label));

    def getValueAsInt(self, label: str) -> int:
        return int(self.getValue(label));

    def getValueAsFloat(self, label: str) -> float:
        return float(self.getValue(label));

    def getValueAsString(self, label: str) -> str:
        return str(self.getValue(label));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Arguments
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Arguments:
    __arguments: Dict[str, Argument];

    def __init__(self):
        self.__arguments = dict();
        return;

    def __iter__(self):
        for label in self.__arguments:
            yield label, self.__arguments[label];

    def __len__(self) -> int:
        return len(self.__arguments);

    def __str__(self):
        return str(dict(tokens=self.tokens, values=str(self.kwvalues)));

    @property
    def tokens(self) -> List[str]:
        return [label for label, argument in self.__iter__() if not argument.takes_value and argument.value];

    @property
    def kwvalues(self) -> ArgumentValues:
        return ArgumentValues(**{label: argument.multivalue for label, argument in self.__iter__() if argument.takes_value});

    @property
    def values(self) -> ArgumentValues:
        return ArgumentValues(**{label: argument.multivalue for label, argument in self.__iter__()});

    @property
    def state(self) -> List[Tuple[str, List[Validity], Argument]]:
        return [(label, argument.state, argument) for label, argument in self.__iter__()];

    def add(self, label: str, argument: Argument):
        if label in self.__arguments:
            del self.__arguments[label];
        self.__arguments[label] = argument;

    def parse(self, *args: str):
        tokens, kwargs, ksargs = parse_cli_args(*args, strict=True, ignorecase=False);
        for _, argument in self.__iter__():
            if argument.takes_value:
                valid, values = parse_one_kw(argument, kwargs, ksargs);
            else:
                values = [parse_one_token(argument, tokens)];
                valid = True;
            argument.multivalue.items = values;
            argument.multivalue.valid = valid
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

def display_value_type(value_type: FlatType) -> str:
    as_string = type_to_string(value_type);
    if as_string is None:
        return '';
    elif isinstance(as_string, str):
        return as_string;
    else:
        return ' | '.join([ display_value_type(x) for x in as_string if not x is None ]);

def display_command(typ: str, key: Key, value_type: FlatType, required: bool) -> str:
    key_ = display_key(key);
    if typ in ['key-value', 'key-space-value']:
        sep = ' ' if typ == 'key-space-value' else '=';
        value_type_ = display_value_type(value_type);
        command = '{key}{sep}{value_type}'.format(key=key_, sep=sep, value_type=value_type_);
    else:
        command = key_;
    return command if required else '[ {} ]'.format(command);

# separates cli arguments into tokens, key-value arguments, and key-space-value arguments,
# whilst retaining the order and duplicate key-(space-)value arguments.
# Use strict=False to remove leading -'s from keys.
# Use ignorecase=True to place all keys in lower case.
def parse_cli_args(*args: str, strict=True, ignorecase=True) -> Tuple[List[str], Dict[str, List[str]], Dict[str, List[str]]]:
    tokens = [];
    kwargs = dict();
    ksargs = dict();

    def clean_key(key: str) -> str:
        if not strict:
            key = re.sub(r'^\-*', '', key);
        if ignorecase:
            key = key.lower();
        return key;

    n = len(args);
    first_run = [];
    for k, arg in enumerate(args):
        m = re.match(r'^(.*?)\=(.*)$', arg);
        if not m:
            first_run.append((k, False, arg, None));
        else:
            key = m.group(1);
            value = m.group(2);
            first_run.append((k, True, key, value));

    for k, is_kwarg, key, value in first_run:
        label = clean_key(key);
        if is_kwarg:
            if not label in kwargs:
                kwargs[label] = [];
            kwargs[label].append(value);
        else:
            tokens.append(label);
            # get next value, provided next argument ist not a kwarg:
            if k < n-1 and re.match(r'^(-+)', key):
                _, is_kwarg_next, value, _ = first_run[k+1];
                if not is_kwarg_next:
                    if not key in kwargs:
                        ksargs[label] = [];
                    ksargs[label].append(value);
    return tokens, kwargs, ksargs;
