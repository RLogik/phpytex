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
    "FinalProperty",
    "Property",
    "TriggerProperty",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS
# ----------------------------------------------------------------

T = TypeVar("T")

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class PropertyBase(Generic[T]):
    _final: bool

    def __init__(self, factory: Callable[[], T] | None, final: bool):
        self._final = final
        self._factory = factory

    def __call__(self) -> T:
        if not hasattr(self, "_value") and callable(self._factory):
            self._value = self._factory()
        if not hasattr(self, "_value"):
            raise AssertionError("Call ... .value = ... first!")
        return self._value

    def set(self, x: T):
        if self._final and hasattr(self, "_value"):
            raise AssertionError("Can only set value once!")
        self._value = x


class Property(PropertyBase[T]):
    """
    A class allowing delayed setting of properties.

    Property clases are type-annotated

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

    Property instances are not final, i.e. can be set multiple times

    ```py
    temperature = Property[float]()
    temperature.set(273.15)
    temperature.set(0.15) # allowed
    ```

    Can set a factory method

    ```py
    name = Property[str](lambda: 'Max Mustermann')
    Property(value) # 'Max Mustermann'
    ```

    If a factory method is set,
    then setting the value can still override it:

    ```py
    # .set takes precendence
    name = Property[str](lambda: 'Max Mustermann')
    name.set('Julia Musterfrau')
    print(name()) # 'Julia Musterfrau'

    # .set overrides factory value
    name = Property[str](lambda: 'Max Mustermann')
    print(name()) # 'Max Mustermann'
    name.set('Julia Musterfrau') # allowed
    print(name()) # 'Julia Musterfrau'
    ```
    """

    def __init__(self, factory: Callable[[], T] | None = None):
        super(PropertyBase[T], self).__init__(factory=factory, final=False)


class FinalProperty(PropertyBase[T]):
    """
    A class allowing delayed setting of properties.

    FinalProperty classes are type-annotated

    ```py
    temperature = FinalProperty[float]() # final property of type <float>
    ...
    value = temperature() # variable 'value' shows up with intellisense as type <float>
    ```

    To set and get value, use as follows

    ```py
    temperature = FinalProperty[float]()
    temperature.set(273.15)
    value = temperature()
    print(value) # 273.15
    ```

    FinalProperty instances are final, i.e. can only be set once

    ```py
    temperature = FinalProperty[float]()
    temperature.set(273.15)
    temperature.set(0.15) # raises error
    ```

    Can set a factory method

    ```py
    name = FinalProperty[str](lambda: 'Max Mustermann')
    FinalProperty(value) # 'Max Mustermann'
    ```

    If a factory method is set,
    then setting the value can still override it:

    ```py
    # .set takes precendence
    name = FinalProperty[str](lambda: 'Max Mustermann')
    name.set('Julia Musterfrau')
    print(name()) # 'Julia Musterfrau'

    # factory takes precendence
    name = FinalProperty[str](lambda: 'Max Mustermann')
    print(name()) # 'Max Mustermann'
    name.set('Julia Musterfrau') # raises error
    ```
    """

    def __init__(self, factory: Callable[[], T] | None = None):
        super().__init__(factory=factory, final=True)


class Property(PropertyBase[T]):
    """
    A class allowing delayed setting of properties.

    Property clases are type-annotated

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

    Property instances are not final, i.e. can be set multiple times

    ```py
    temperature = Property[float]()
    temperature.set(273.15)
    temperature.set(0.15) # allowed
    ```

    Can set a factory method

    ```py
    name = Property[str](lambda: 'Max Mustermann')
    Property(value) # 'Max Mustermann'
    ```

    If a factory method is set,
    then setting the value can still override it:

    ```py
    # .set takes precendence
    name = Property[str](lambda: 'Max Mustermann')
    name.set('Julia Musterfrau')
    print(name()) # 'Julia Musterfrau'

    # .set overrides factory value
    name = Property[str](lambda: 'Max Mustermann')
    print(name()) # 'Max Mustermann'
    name.set('Julia Musterfrau') # allowed
    print(name()) # 'Julia Musterfrau'
    ```
    """

    def __init__(self, factory: Callable[[], T] | None = None):
        super().__init__(factory=factory, final=False)


class TriggerProperty:
    """
    Use to set a boolean value to `true` and maintain this value.
    Initialises as false.
    """

    _value: Property[bool]

    def __init__(self):
        self._value = False

    @property
    def value(self):
        return self._value

    def __call__(self) -> bool:
        return self._value

    def set(self):
        """
        Permanently sets trigger value to `true`.
        """
        self._value = True
