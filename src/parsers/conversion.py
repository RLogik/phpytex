#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.models.internal import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'convert_to_python_string',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD convert variable to python string
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def convert_to_python_string(value: Any) -> str:
    if isinstance(value, str):
        lines = re.split(r'\n', value);
        if len(lines) > 1:
            sep = r"+'\n'+";
            return sep.join(["r'{}'".format(_) for _ in lines]);
        return "r'{}'".format(value);
    elif isinstance(value, (int, float, bool, EvalType)) or value is None:
        return str(value);
    elif isinstance(value, tuple):
        values = [
            convert_to_python_string(value=_)
            for _ in value
        ];
        return '({})'.format(', '.join(values));
    elif isinstance(value, list):
        sepFirst = sepComma = sepFinal = '';
        return '[{sepFirst}{contents}{sepFinal}]'.format(
            sepFirst = sepFirst,
            contents = (', ' + sepComma).join([
                convert_to_python_string(x)
                for x in value
            ]),
            sepFinal = sepFinal,
        );
    elif isinstance(value, dict):
        sepFirst = sepComma = sepFinal = '';
        return '{{{sepFirst}{contents}{sepFinal}}}'.format(
            sepFirst = sepFirst,
            contents = (', ' + sepComma).join([
                "'{key}': {value}".format(
                    key   = key,
                    value = convert_to_python_string(x),
                ) for key, x in value.items()
            ]),
            sepFinal = sepFinal,
        );
    raise Exception('Could not evaluated value as string');
