#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any;
from typing import List;
from typing import Union;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class ValueType
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ValueType:
    value: Any;
    __valuetype: Union[type, list, None];

    def __init__(self, valuetype=None, value=None, **kwargs):
        self.value = value;
        self.__valuetype = valuetype;

    def matchestype(self, o: Any) -> bool:
        t = self.__valuetype;
        if t is None:
            return True;
        elif isinstance(t, type):
            return type(o) == t;
        elif isinstance(t, list):
            return o in t;
        return False;

    def __str__(self):
        return str(self.value);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class MultiValueType
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MultiValueType:
    default: Any;
    items: List[Any];
    __valid_force_set: bool = False;
    __valid: bool;
    __valuetype: Union[type, list, None];

    def __init__(self, valid=None, items=[], item=None, default=None, valuetype=None, **kwargs):
        self.default = default;
        self.__valuetype = valuetype;

        if not item is None:
            self.items = [item];
        else:
            self.items = items[:];

        self.__valid_force_set = False;
        if isinstance(valid, bool):
            self.valid = valid;

    def __iter__(self):
        for _ in self.items:
            yield _;

    def __len__(self) -> int:
        return len(self.items);

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
        if len(self.items) > 0:
            return self.items[0];
        return self.default;

    @property
    def values(self):
        return self.items;

    @property
    def valid(self) -> bool:
        if self.__valid_force_set:
            return self.__valid;
        return self.matchestype(self.value);

    @valid.setter
    def valid(self, x: bool):
        self.__valid = x;
        self.__valid_force_set = True;

    @property
    def all_valid(self) -> List[bool]:
        return [self.matchestype(item) for item in self.__iter__()];

    def matchestype(self, o: Any) -> bool:
        t = self.__valuetype;
        if t is None:
            return True;
        elif isinstance(t, type):
            return type(o) == t;
        elif isinstance(t, list):
            return o in t;
        return False;
