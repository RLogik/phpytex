#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from typing import Callable
from typing import Generic
from typing import TypeVar

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'Property',
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS
# ----------------------------------------------------------------

T = TypeVar('T')

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class Property(Generic[T]):
    '''
    A class allowing delayed setting of properties.

    Properties are type-annotated

    ```py
    temperature = Property[float]() # property of type <float>
    ...
    value = temperature() # variable 'value' shows up with intellisense as type <float>
    ```

    To set and get value, use as follows

    ```py
    temperature = Property[float]()
    temperature.set(273.15)
    value = temperature()
    print(value) # 273.15
    ```

    By default properties are final, i.e. can only be set once

    ```py
    temperature1 = Property[float]()
    temperature2 = Property[float](final=True) # default
    temperature3 = Property[float](final=False)

    temperature1.set(273.15)
    temperature2.set(273.15)
    temperature3.set(273.15)

    temperature3.set(0.15) # allowed
    temperature1.set(0.15) # raises error
    temperature2.set(0.15) # raises error
    ```

    Can set a factory method

    ```py
    name = Property[str](lambda: 'Max Mustermann')
    print(value) # 'Max Mustermann'
    ```

    If a property a factory method is set,
    then setting the value can still override it:

    ```py
    # .set takes precendence
    name = Property[str](lambda: 'Max Mustermann')
    name.set('Julia Musterfrau')
    print(name()) # 'Julia Musterfrau'

    # factory takes precendence
    name = Property[str](lambda: 'Max Mustermann')
    print(name()) # 'Max Mustermann'
    name.set('Julia Musterfrau') # raises error
    ```
    '''

    _final: bool

    def __init__(self, factory: Callable[[], T] | None = None, final: bool = True):
        self._final = final
        self._factory = factory

    def __call__(self) -> T:
        if not hasattr(self, '_value') and callable(self._factory):
            self._value = self._factory()
        if not hasattr(self, '_value'):
            raise AssertionError('Call <property>.set(<value>) first!')
        return self._value

    def set(self, x: T):
        if self._final and hasattr(self, '_value'):
            raise AssertionError('Can only set value once!')
        self._value = x
