#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

from typing import Any
from typing import Generic
from typing import TypeVar

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "ConfigParameter",
]

# ----------------------------------------------------------------
# GLOBAL VARIABLES
# ----------------------------------------------------------------

_T = TypeVar("_T")
# bound='<name-of-class>');

# ----------------------------------------------------------------
# CLASS config parameter - for internal config parameters
# ----------------------------------------------------------------


class ConfigParameter(Generic[_T]):
    _name: str
    _defaultvalue: _T
    _value: _T
    _is_set: bool

    def __init__(self, name: str):
        self._name = name
        self._is_set = False
        return

    def __str__(self) -> str:
        return str(self.value)

    def getType(self) -> type:
        return self.__orig_class__.__args__[0]

    @property
    def hasValue(self) -> bool:
        return self._is_set

    @property
    def value(self) -> _T:
        if self.hasValue and hasattr(self, "_value"):
            return self._value
        elif hasattr(self, "_defaultvalue"):
            return self._defaultvalue
        raise Exception(
            "For internal app parameter \033[1m{}\033[0m no value or default value is set!".format(
                self._name
            )
        )

    @value.setter
    def value(self, x: Any):
        self._is_set = False
        if isinstance(x, self.getType()):
            self._is_set = True
            self._value = x
        return

    def setValue(self, x: Any) -> ConfigParameter[_T]:
        self._defaultvalue = x
        self.value = x
        return self
