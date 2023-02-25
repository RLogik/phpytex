#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.types import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'DictionaryWithDefault',
    'factory_dictionary_str_any_none',
    'factory_dictionary_str_bool_false',
    'factory_dictionary_str_int_zero',
    'property_inheritance_graph',
    'get_roots_graph',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOCAL VARIABLES / CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KT = TypeVar('KT');
VT = TypeVar('VT');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS DictionaryWithDefault
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DictionaryWithDefault(dict[KT, VT]):
    '''
    Extends a dictionary like object with default value for missing keys.

    ## Usage ##

    ```py
    options: DictionaryForce[str, bool] = DictionaryForce(default=False);
    option['easy'] = True;
    print(option['easy']); # True
    print(option['randomise']); # False, since key not set
    ```
    '''
    default_factory: Callable[[], VT];

    def __init__(
        self,
        default: Optional[VT] = None,
        default_factory: Optional[Callable[[], VT]] = None,
    ):
        super().__init__();
        if default_factory is None:
            self.default_factory = lambda: default;
        return;

    def __getitem__(self, key: KT) -> VT:
        if key not in self.keys():
            self.__setitem__(key, self.default_factory());
        return self.get(key, self.default_factory());

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Factories
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def factory_dictionary_str_any_none() -> DictionaryWithDefault[str, Any]:
    return DictionaryWithDefault(default=None);

def factory_dictionary_str_bool_false() -> DictionaryWithDefault[str, bool]:
    return DictionaryWithDefault(default=False);

def factory_dictionary_str_int_zero() -> DictionaryWithDefault[str, int]:
    return DictionaryWithDefault(default=0);
