#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
from typing import Any;
from typing import Dict;
from typing import List;
from typing import Tuple;
from typing import Union;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Decorator: @static
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class static(object):
    '''
    Emulates 'public static final'
    '''
    def __init__(self, fget):
        self.fget = fget;

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls);

    def __set__(self, instance, value):
        raise ValueError();

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

def parse_cli_args(args: List[str]) -> Tuple[List[str], Dict[str, str]]:
    tokens = [];
    kwargs = {};
    for arg in args:
        m = re.match(r'^(.*?)\=(.*)$', arg);
        if not m:
            arg = re.sub(r'^\-*', '', arg);
            arg = arg.lower();
            tokens.append(arg);
        else:
            key = m.group(1);
            value = m.group(2);
            kwargs[key] = value;
    return tokens, kwargs;

def get_dict_value(obj: Any, key: str, *keys: str, default: Any = None):
    obj_ = obj[key] if isinstance(obj, dict) and key in obj else default;
    return obj_ if len(keys) == 0 else get_dict_value(obj_, *keys);
