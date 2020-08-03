#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re
from typing import Any;
from typing import List;
from typing import Tuple;
from typing import Union;

from ..types.file import FileType;
from ..types.path import PathType;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Type: FlattenedType
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FlatType = Union[type, None, str, List[Union[type, None, str]]];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def string_to_type(s: Union[str, None, List[str]]) -> FlatType:
    if isinstance(s, str):
        s = s.lower();
        if s in ['int', 'integer']:
            return int;
        if s in ['float', 'number', 'numeric']:
            return float;
        if s in ['bool', 'boolean']:
            return bool;
        if s in ['str', 'string']:
            return str;
        if s in ['file']:
            return FileType;
        if s in ['path', 'dir', 'directory']:
            return PathType;
        if re.match(r'^None$', s, re.IGNORECASE):
            return None;
        return s;
    elif s is None:
        return None;
    else:
        t = [];
        for s_ in s:
            tt = string_to_type(s_);
            if isinstance(tt, list):
                t += tt;
            else:
                t.append(tt);
        return t;

########
# NOTE: Do not write type of output!
# In this case, python is incapable of recognising validity.
# Externally, however, other commands correctly recognise the type as
#   Union[None, str, List[Union[None, str]]].
########
def type_to_string(t: FlatType):
    if isinstance(t, type):
        return "<{}>".format(t.__name__);
    elif t is None:
        return None;
    elif isinstance(t, str):
        return "{}".format(t);
    else:
        return [type_to_string(tt) for tt in t];

def parse_type(value: str, value_type: FlatType) -> Tuple[Any, bool]:
    if value_type is None:
        return value, True;
    elif isinstance(value_type, type):
        if value_type == bool:
            if re.match('^(true|1|y|yes|j|ja)$', value, re.IGNORECASE):
                return True, True;
            elif re.match('^(false|0|n|no|nein)$', value, re.IGNORECASE):
                return False, True;
        elif value_type in [int, float, str]:
            try:
                value_ = value_type(value);
                return value_, True;
            except:
                return None, False;
        elif value_type == FileType:
            if isinstance(value, FileType):
                return FileType(value), True;
        elif value_type == PathType:
            if isinstance(value, PathType):
                return PathType(value), True;
    elif isinstance(value_type, str):
        value_ = value_type;
        if value == value_:
            return value_, True;
    elif isinstance(value_type, list):
        parsed = [parse_type(value, value_type_) for value_type_ in value_type];
        for value_, accept in parsed:
            if accept:
                return value_, True;
    return None, False;
