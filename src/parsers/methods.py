#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
from typing import Any;
from typing import Union;
from typing import Tuple;

from src.customtypes.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD escape string for use in python code
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def escapeForPython(s: str) -> str:
    s = re.sub(r'(\\+)', r'\1\1', s);
    s = re.sub(r'\n', r'\\n', s);
    s = re.sub(r'\t', r'\\t', s);
    s = re.sub(r'\"', r'\\u0022', s);
    s = re.sub(r'\'', r'\\u0027', s);
    # s = re.sub(r'\%', slash+'u0025', s);
    s = re.sub(r'(\{+)', r'\1\1', s);
    s = re.sub(r'(\}+)', r'\1\1', s);
    return s;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD convert variable to python string
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def convertToPythonString(
    value:      Any,
    indent:     int  = 0,
    multiline:  bool = False,
    indentchar: str  = '    '
) -> Tuple[Union[str, None], str]:
    typ = None;
    if isinstance(value, str):
        typ = 'str';
        lines = re.split(r'\n', value);
        if len(lines) > 1:
            sep = "\n{}".format(indentchar*indent) if multiline else r"+'\n'+";
            return typ, sep.join(["r'{}'".format(_) for _ in lines]);
        return typ, "r'{}'".format(value);
    elif isinstance(value, (int, float, bool, EvalType)) or value is None:
        if isinstance(value, int):
            typ = 'int';
        elif isinstance(value, float):
            typ = 'float';
        elif isinstance(value, bool):
            typ = 'bool';
        return typ, str(value);
    elif isinstance(value, tuple):
        typ = 'tuple';
        values = [convertToPythonString(_, indent+1, multiline)[1] for _ in value];
        if multiline and len(values) > 1:
            sep0 = "\n{}".format(indentchar*indent);
            sep1 = "\n{}".format(indentchar*(indent+1));
            return typ, '[' +  sep1 \
                + (',' + sep1).join(values) + ',' \
                + sep0 + ']';
        return typ, '({})'.format(', '.join(values));
    elif isinstance(value, list):
        typ = 'list';
        values = [convertToPythonString(_, indent+1, multiline)[1] for _ in value];
        if multiline and len(values) > 1:
            sep0 = "\n{}".format(indentchar*indent);
            sep1 = "\n{}".format(indentchar*(indent+1));
            return typ, '[' +  sep1 \
                + (',' + sep1).join(values) + ',' \
                + sep0 + ']';
        return typ, '[{}]'.format(', '.join(values));
    elif isinstance(value, dict):
        typ = 'dict';
        values = [(_, convertToPythonString(value[_], indent+1, multiline)[1]) for _ in value];
        if multiline and len(values) > 1:
            sep0 = "\n{}".format(indentchar*indent);
            sep1 = "\n{}".format(indentchar*(indent+1));
            return typ, '{' +  sep1 \
                + (',' + sep1).join(["'{}': {}".format(_, __) for _, __ in values]) + ',' \
                + sep0 + '}';
        return typ, '{' + ', '.join(["'{}': {}".format(_, __) for _, __ in values]) + '}';
    raise Exception('Could not evaluated value as string');
