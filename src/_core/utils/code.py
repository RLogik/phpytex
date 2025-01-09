#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from functools import wraps
from typing import Any
from typing import Callable
from typing import Generic
from typing import ParamSpec
from typing import TypeVar
from typing import overload

from lazy_load import lazy
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from safetywrap import Err
from safetywrap import Ok
from safetywrap import Result

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "TypeGuard",
    "compute_once",
    "make_lazy",
    "make_safe",
    "make_safe_none",
    "value_of_model",
    "wrap_result",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS, VARIABLES
# ----------------------------------------------------------------

PARAMS = ParamSpec("PARAMS")
RETURN = TypeVar("RETURN")
T = TypeVar("T")
E = TypeVar("E")
ERR = TypeVar("ERR", bound=BaseException)
MODEL = TypeVar("MODEL", bound=BaseModel)

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def make_lazy(method: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN]:
    """
    Decorates a method and makes it return a lazy-load output.
    """

    @wraps(method)
    def wrapped_method(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
        return lazy(method, *_, **__)

    return wrapped_method


def compute_once(method: Callable[[], RETURN]) -> Callable[[], RETURN]:
    """
    Decorates a possibly expensive method to ensure that it only computes once
    and thereafter simply returns an internally stored value.

    If for some reason the value is destroyed, then recomputes this.
    """
    _value = None
    _first = True

    @wraps(method)
    def wrapped_method() -> RETURN:
        nonlocal _value
        nonlocal _first
        if _first or _value is None:
            _value = method()
        _first = False
        return _value

    return wrapped_method


def value_of_model(m: MODEL):
    return m.root


@overload
def wrap_result(
    method: Callable[PARAMS, Result[RETURN, ERR]],
    /,
) -> Callable[PARAMS, Result[RETURN, ERR]]: ...


@overload
def wrap_result(
    method: Callable[PARAMS, RETURN],
    /,
) -> Callable[PARAMS, Result[RETURN, Exception]]: ...


def wrap_result(
    method: Callable[PARAMS, RETURN]
    | Callable[PARAMS, Result[RETURN, ERR]]
    | Callable[PARAMS, RETURN | Result[RETURN, ERR]],  # fmt: skip
    /,
) -> Callable[PARAMS, Result[RETURN, Exception]] | Callable[PARAMS, Result[RETURN, ERR]]:
    """
    Uses the Ok/Err to wrap a method `f`.
    Flattens any Ok/Err in the process

    | outcome of `f` | outcome of wrapped |
    | :------------- | :----------------- |
    | returns `Ok(x)` | returns `Ok(x)` |
    | returns `Err(x)` | returns `Err(x)` |
    | returns `x` | returns `Ok(x)` |
    | raises Exception err | returns `Err(err)` |
    | raises BaseException err | raises `err` |
    """

    @wraps(method)
    def wrapped_fct(*_: PARAMS.args, **__: PARAMS.kwargs):
        try:
            value = method(*_, **__)
            if isinstance(value, Result):
                return value
            return Ok(value)

        except Exception as err:
            return Err(err)

        except BaseException as err:
            raise err

    return wrapped_fct


def safe_unwrap(
    method: Callable[[], RETURN],
    default: E = None,
    default_factory: Callable[[], E] | None = None,
) -> RETURN | E:
    """
    Calls method and returns default if exception raised.
    Only raises error in the case of interruptions/sys exit.
    """
    try:
        result = method()
        return result

    except BaseException as err:
        if isinstance(err, (KeyboardInterrupt, EOFError, SystemExit)):
            raise err

    if default_factory is not None:
        result = default_factory()
        return result

    return default


def make_safe(
    default: E | None = None,
    default_factory: Callable[[], E] | None = None,
):
    """
    Decorator which modifies funcitons
    to make them return default values upon exceptions.
    """

    def dec(f: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN | E]:
        @wraps(f)
        def wrapped_fct(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN | E:
            return safe_unwrap(
                lambda: f(*_, **__),
                default=default,
                default_factory=default_factory,
            )

        return wrapped_fct

    return dec


def make_safe_none(f: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN | None]:
    """
    Decorator which modifies funcitons
    to make them return the default value None upon exceptions.
    """

    @wraps(f)
    def wrapped_fct(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN | None:
        return safe_unwrap(lambda: f(*_, **__))

    return wrapped_fct


class TypeGuard(BaseModel, Generic[T, E]):
    """
    Provides a method that asserts type or else returns a default value.

    The default of `default` is `null`.

    ## Usage ##
    ```py
    coerce = TypeGuard[int, None](type=int)
    coerce(5) # 5
    coerce("cat") # None

    coerce = TypeGuard[int, int](type=int, default=-1)
    coerce(5) # 5
    coerce("cat") # -1

    coerce = TypeGuard[int, int](type=int, default_factory=lambda x: len(x))
    coerce(5) # 5
    coerce("cat") # 3

    coerce = TypeGuard[int, str](type=int, default_factory=str)
    coerce(5) # 5
    coerce("cat") # "cat"
    coerce(7.1) # "7.1"
    ```
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: type = Field(..., alias="type")
    default_: E | None = Field(default=None, alias="default")
    default_factory_: Callable[[Any], E | None] | None = Field(
        default=None, alias="default_factory"
    )

    def __call__(self, x: Any, /) -> T | E | None:
        if isinstance(x, self.type_):
            return x
        f = self.default_factory_
        if self.default_factory_ is None:
            return self.default_
        return f(x)
