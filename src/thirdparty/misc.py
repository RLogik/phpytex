#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from datetime import datetime;
from datetime import timedelta;
from functools import wraps;
from itertools import chain as itertools_chain;
import lorem;
import re;
from textwrap import dedent as textwrap_dedent;
from typing import Callable;
from typing import TypeVar;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODIFICATIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

T = TypeVar('T');

def prestrip(first: bool = True, last: bool = True, all: bool = False):
    '''
    Returns a decorator that modifies string -> string methods
    '''
    T_ = TypeVar('T_');
    def dec(method: Callable[[str], T_]) -> Callable[[str], T_]:
        '''
        Performs method but first strips initial/final (empty) lines.
        '''
        @wraps(method)
        def wrapped_method(text: str) -> T_:
            lines = re.split(pattern=r'\n', string=text);
            if all:
                if first:
                    while len(lines) > 0 and lines[0].strip() == '':
                        lines = lines[1:];
                if last:
                    while len(lines) > 0 and lines[-1].strip() == '':
                        lines = lines[:-1];
            else:
                if first:
                    lines = lines[1:];
                if last:
                    lines = lines[:-1];
            text = '\n'.join(lines);
            return method(text);
        return wrapped_method;
    return dec;

@prestrip(all=False)
def dedent(text: str) -> str:
    '''
    Remove any common leading whitespace from every line in `text`.

    This can be used to make triple-quoted strings line up with the left
    edge of the display, while still presenting them in the source code
    in indented form.

    Note that tabs and spaces are both treated as whitespace, but they
    are not equal: the lines "  hello" and "\\thello" are
    considered to have no common leading whitespace.

    Entirely blank lines are normalized to a newline character.
    '''
    return textwrap_dedent(text);


def dedent_as_list(text: str) -> list[str]:
    '''
    Performs the `dedent` function and returns lines as a list.
    '''
    return re.split(r'\n', dedent(text));

def flatten(XX: list[list[T]]) -> list[T]:
    return list(itertools_chain.from_iterable(XX));

def unique(X: list[T]) -> list[T]:
    return list(set(X));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'datetime',
    'dedent',
    'dedent_as_list',
    'flatten',
    'lorem',
    'prestrip',
    're',
    'timedelta',
    'unique',
];
