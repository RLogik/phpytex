#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
from typing import Any;
from typing import List;
from typing import Union;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Decorator: @static
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class static(object):
    ### Emulates 'public static final
    def __init__(self, fget):
        self.fget = fget;

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls);

    def __set__(self, instance, value):
        raise ValueError();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Inf
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Inf:
    @static
    def value(cls):
        return float('inf');

    @staticmethod
    def not_inf(x: Any):
        return isinstance(x, (int, float)) and x < Inf.value;

    # assumption: #
    def __gt__(self, other):
        return Inf.not_inf(other);

    def __ge__(self, other):
        return True;

    def __lt__(self, other):
        return False;

    def __le__(self, other):
        return not Inf.not_inf(other);

    def ___eq__(self, other):
        return not Inf.not_inf(other);

    def ___ne__(self, other):
        return Inf.not_inf(other);

    def __str__(self):
        return 'inf';

    def __format__(self, fmt):
        return 'inf';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constant: INFINITY
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INFINITY = Inf();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def clean_string(s: str, trim: bool = False) -> str:
    s = '' if s is None else s;
    return s if not trim else re.sub(r'^\s*|\s*$', '', s);

def truncate_string(s: str, max_length: Union[int, None] = None) -> str:
    if len_pure(s) > max_length:
        s = s[:(max_length-3)] + r'...';
    return s;

def purify(s: str) -> str:
    return re.sub(r'\x1b[^m]*m', '', s);

def len_pure(s: str) -> int:
    return len(purify(s));

def pad_string(s: str, n: int, sep=' ') -> str:
    m = len_pure(s);
    if n > m:
        s += sep*(n-m);
    return s;

def pad_strings(*lines: str, sep=' ') -> List[str]:
    N = len(lines);
    lengths = [len_pure(s) for s in lines];
    L = max(lengths);
    return [lines[k] + sep*(L-lengths[k]) for k in range(N)];

def to_cli_key(label):
    return re.sub(r'_', '-', label);

def to_python_key(label):
    return re.sub(r'-', '_', label);
