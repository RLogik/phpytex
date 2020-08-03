#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from copy import deepcopy;
from typing import Dict;
from typing import Type;

from ..values.valuetypes import ValueType

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class ConfigurableAttributes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ConfigurableAttributes:
    def __getattr__(self, key: str):
        if not hasattr(self, key):
            raise KeyError('The attribute {} was not defined.'.format(key));
        return getattr(self, key);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class Configurable
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Configurable(ConfigurableAttributes):
    _DEFAULT: Dict[str, ValueType] = dict();

    def __init__(self, *args, **kwargs):
        return;

    def __str__(self):
        return str({key: str(value) for key, value, _ in self.__iter__()});

    def __iter__(self):
        for key in self._DEFAULT:
            yield key, getattr(self, key), self._DEFAULT[key].value;

    def __contains__(self, key: str) -> bool:
        return key in self._DEFAULT;

    def __getattr__(self, key: str):
        return super().__getattr__(key);

    def __setattr__(self, key: str, value):
        if not self.__contains__(key):
            raise KeyError('The attribute {} cannot be defined.'.format(key));
        ## NOTE: need super() to pevent infinite recursion:
        value_ = value if self._DEFAULT[key].matchestype(value) else self._DEFAULT[key].value;
        super().__setattr__(key, value_);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Decorator: @transfer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def transfer(cls: Type[Configurable]):
    ### Transfers dictionary like attributes to a class
    def __init__(self, *args, **kwargs):
        for key in cls._DEFAULT:
            default = cls._DEFAULT[key];
            self.__setattr__(key, deepcopy(kwargs[key]) if key in kwargs else default.value);
    cls.__init__ = __init__;
    return cls;
