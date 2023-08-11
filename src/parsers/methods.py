#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.misc import *;
from src.local.maths import *;
from src.local.config import *;
from src.local.typing import *;

from src.customtypes.exports import *;

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
        return typ, json.dumps(value);
    elif isinstance(value, (int, float, bool, EvalType)) or value is None:
        if isinstance(value, int):
            typ = 'int';
        elif isinstance(value, float):
            typ = 'float';
        elif isinstance(value, bool):
            typ = 'bool';
        return typ, str(value);
    elif isinstance(value, Fraction):
        return 'Fraction', f"Fraction('{value}')",
    elif isinstance(value, tuple):
        typ = 'tuple';
        values = [convertToPythonString(value=_, indent=indent+1, multiline=multiline)[1] for _ in value];
        if multiline and len(values) > 1:
            sep0 = "\n{}".format(indentchar*indent);
            sep1 = "\n{}".format(indentchar*(indent+1));
            return typ, '[' +  sep1 \
                + (',' + sep1).join(values) + ',' \
                + sep0 + ']';
        return typ, '({})'.format(', '.join(values));
    elif isinstance(value, list):
        typ = 'list';
        sepFirst = sepComma = sepFinal = '';
        if multiline and len(value) > 1:
            sepFirst = '\n{}'.format(indentchar*(indent+1));
            sepComma = '\n{}'.format(indentchar*(indent+1));
            sepFinal = ',\n{}'.format(indentchar*indent);
        return typ, '[{sepFirst}{contents}{sepFinal}]'.format(
            sepFirst = sepFirst,
            contents = (',' + sepComma).join([ convertToPythonString(x, indent=indent+1, multiline=multiline)[1] for x in value ]),
            sepFinal = sepFinal,
        );
    elif isinstance(value, dict):
        typ = 'dict';
        sepFirst = sepComma = sepFinal = '';
        if multiline and len(value) > 1:
            sepFirst = '\n{}'.format(indentchar*(indent+1));
            sepComma = '\n{}'.format(indentchar*(indent+1));
            sepFinal = ',\n{}'.format(indentchar*indent);
        return typ, '{{{sepFirst}{contents}{sepFinal}}}'.format(
            sepFirst = sepFirst,
            contents = (',' + sepComma).join([
                "'{key}': {value}".format(
                    key   = key,
                    value = convertToPythonString(x, indent=indent+1, multiline=multiline)[1],
                ) for key, x in value.items()
            ]),
            sepFinal = sepFinal,
        );
    raise Exception('Could not evaluated value as string');
