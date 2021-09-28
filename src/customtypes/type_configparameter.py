#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.local.typing import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_T = TypeVar('_T'); #bound='<name-of-class>');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS config parameter - for internal config parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ConfigParameter(Generic[_T]):
    _defaultvalue: _T;
    _value: _T;

    def __str__(self) -> str:
        return str(self.value);

    def getType(self) -> type:
        return self.__orig_class__.__args__[0];

    @property
    def value(self) -> _T:
        if hasattr(self, '_value'):
            return self._value;
        elif hasattr(self, '_defaultvalue'):
            return self._defaultvalue;
        raise Exception('No value or default value set!');

    @value.setter
    def value(self, x: Any):
        if isinstance(x, self.getType()):
            self._value = x;
        return;

    def setValue(self, x: Any) -> ConfigParameter[_T]:
        self.value = x;
        return self;
