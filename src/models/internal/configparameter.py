#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.thirdparty.types import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

T = TypeVar('T'); #bound='<name-of-class>');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS config parameter - for internal config parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ConfigParameter(Generic[T]):
    _value: Optional[T];

    def __init__(self):
        self._value = None;
        return;

    def __str__(self) -> str:
        return str(self.value);

    def getType(self) -> type:
        return self.__orig_class__.__args__[0];

    @property
    def value(self) -> T:
        if self._value is not None:
            return self._value;
        raise Exception(f'No value set for internal app parameter \033[1m{self._name}\033[0m.');

    @value.setter
    def value(self, x: T):
        self._value = x;
        return;

    def setValue(self, x: Any) -> ConfigParameter[T]:
        self.value = x;
        return self;
