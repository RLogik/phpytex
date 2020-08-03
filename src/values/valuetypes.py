#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any;
from typing import List;
from typing import Union;

from ..types.parse import FlatType;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class ValueType
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ValueType:
    value: Any;
    __valuetype: Union[type, list, None];

    def __init__(self, valuetype=None, value=None, **kwargs):
        self.value = value;
        self.__valuetype = valuetype;

    def matchestype(self, o: Any, main_type=True, t=None) -> bool:
        if main_type:
            t = self.__valuetype;
        if t is None:
            return True;
        elif isinstance(t, type):
            return type(o) == t;
        elif isinstance(t, str):
            return o == t;
        else:
            return True in [self.matchestype(o, False, tt) for tt in t];

    def __str__(self):
        return str(self.value);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class MultiValueType
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MultiValueType:
    default: Any;
    __items: List[Any];
    __valuetype: FlatType;

    def __init__(self, items=[], item=None, default=None, valuetype=None, **kwargs):
        self.default = default;
        self.__valuetype = valuetype;

        if not item is None:
            self.__items = [item];
        else:
            self.__items = items[:];

    def __iter__(self):
        for _ in self.__items:
            yield _;

    def __len__(self) -> int:
        return len(self.__items);

    def __str__(self):
        return str(self.value);

    def __eq__(self, other):
        value = self.value;
        if value is None and other is None:
            return True;
        elif value is None or other is None:
            return False;
        return value == other;

    @property
    def value(self):
        if len(self.__items) > 0:
            return self.__items[0];
        return self.default;

    @property
    def values(self):
        return self.__items;

    @values.setter
    def values(self, x: list):
        self.__items = x;

    @property
    def valid(self) -> bool:
        return not(False in self.all_valid);

    @property
    def all_valid(self) -> List[bool]:
        return [self.matchestype(_) for _ in self.__iter__()];

    def matchestype(self, o: Any, main_type=True, t=None) -> bool:
        if main_type:
            t = self.__valuetype;
        if t is None:
            return True;
        elif isinstance(t, type):
            return type(o) == t;
        elif isinstance(t, str):
            return o == t;
        else:
            return True in [self.matchestype(o, False, tt) for tt in t];
