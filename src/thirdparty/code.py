#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from pydantic import BaseModel
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import Field
from dataclasses import MISSING
from functools import partial
from functools import reduce
from functools import wraps
from itertools import chain as itertools_chain
from itertools import product as itertools_product
from lazy_load import lazy
from operator import itemgetter

# for modifications, not export
# cf. https://github.com/mplanchard/safetywrap
from typing import Callable
from typing import Optional
from typing import ParamSpec
from typing import TypeVar

# ----------------------------------------------------------------
# MODIFICATIONS
# ----------------------------------------------------------------

PARAMS = ParamSpec('PARAMS')
RETURN = TypeVar('RETURN')
E = TypeVar('E')
ERR = TypeVar('ERR', bound=BaseException)
MODEL = TypeVar('MODEL', bound=BaseModel)


def raise_err(err: ERR):
    raise err


def make_lazy(method: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN]:
    '''
    Decorates a method and makes it return a lazy-load output.
    '''

    @wraps(method)
    def wrapped_method(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
        return lazy(method, *_, **__)

    return wrapped_method


def compute_once(method: Callable[[], RETURN]) -> Callable[[], RETURN]:
    '''
    Decorates a possibly expensive method to ensure that it only computes once
    and thereafter simply returns an internally stored value.

    If for some reason the value is destroyed, then recomputes this.
    '''

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


def safe_unwrap(
    method: Callable[[], RETURN],
    default: E = None,
    default_factory: Optional[Callable[[], E]] = None,
) -> RETURN | E:
    '''
    Calls method and returns default if exception raised.
    Only raises error in the case of interruptions/sys exit.
    '''
    try:
        return method()
    except BaseException as err:
        if isinstance(err, (KeyboardInterrupt, EOFError, SystemExit)):
            raise err
    if default_factory is not None:
        return default_factory()
    return default


def make_safe(
    default: E | None = None,
    default_factory: Callable[[], E] | None = None,
):
    '''
    Decorator which modifies funcitons
    to make them return default values upon exceptions.
    '''

    def dec(f: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN | E]:
        @wraps(f)
        def wrapped_fct(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN | E:
            return safe_unwrap(
                lambda: f(*_, **__), default=default, default_factory=default_factory
            )

        return wrapped_fct

    return dec


def make_safe_none(f: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN | None]:
    '''
    Decorator which modifies funcitons
    to make them return the default value None upon exceptions.
    '''

    @wraps(f)
    def wrapped_fct(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN | None:
        return safe_unwrap(lambda: f(*_, **__))

    return wrapped_fct


# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'BaseModel',
    'Field',
    'MISSING',
    'asdict',
    'compute_once',
    'dataclass',
    'field',
    'itemgetter',
    'itertools_chain',
    'itertools_product',
    'lazy',
    'make_lazy',
    'make_safe',
    'make_safe_none',
    'partial',
    'raise_err',
    'reduce',
    'safe_unwrap',
    'value_of_model',
    'wraps',
]
