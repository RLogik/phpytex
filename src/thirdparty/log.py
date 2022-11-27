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

def ansi_formatting(
    use: Optional[bool] = None,
    factory: Optional[Callable[[], bool]] = None,
):
    '''
    Returns a decorator that modifies methods,
    so that string arguments are optionally stripped of ansi characters.

    @inputs
    - `use` - optional <boolean> if `true`, ansi characters will be kept;
      if `false`, ansi characters will be stripped.
    - `factory` - optional <() -> boolean> if set, obtains boolean value from method called dynamically.
    '''
    def dec(method: Callable[..., T]) -> Callable[..., T]:
        '''
        Performs method but first optionally strips ansi characters.
        '''
        @wraps(method)
        def wrapped_method(*texts: str) -> T:
            option = (
                True if factory is None
                else factory()
            ) if use is None else use;
            if option == False:
                texts = [ re.sub(r'\x1b[^m]*m', '', text) for text in texts];
            return method(*texts);
        return wrapped_method;
    return dec;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ansi_formatting',
    'logging',
    'LogRecord',
];
