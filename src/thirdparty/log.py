#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from functools import wraps;
import logging;
from logging import LogRecord;
import re;
from typing import Callable;
from typing import TypeVar;
from typing import Optional;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODIFICATIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

T = TypeVar('T');

def plain_formatting(
    strip: bool = False,
    factory: Optional[Callable[[], bool]] = None,
):
    '''
    Returns a decorator that modifies methods,
    so that string arguments are optionally stripped of ansi characters.

    @inputs
    - `plain` - optional <boolean> if `true`, ansi characters will be stripped.
    - `factory` - optional <() -> boolean> if set, obtains boolean value from method called dynamically.
    '''
    def dec(method: Callable[..., T]) -> Callable[..., T]:
        '''
        Performs method but first optionally strips ansi characters.
        '''
        @wraps(method)
        def wrapped_method(*texts: str) -> T:
            if strip or (False if factory is None else factory()):
                texts = [ re.sub(r'\x1b[^m]*m', '', text) for text in texts];
            return method(*texts);
        return wrapped_method;
    return dec;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'plain_formatting',
    'logging',
    'LogRecord',
];
