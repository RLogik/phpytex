#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any;
from typing import Union;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Validity
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Validity:
    kind: str;
    expected: Any;
    actual: Any;

    def __init__(self, kind: str = None, expected: Any = None, actual: Any = None, **kwargs):
        if not kind is None:
            self.kind = kind;
        if not expected is None:
            self.expected = expected;
        if not actual is None:
            self.actual = actual;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Method
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def display_reason(state: Validity) -> Union[str, None]:
    if state.kind == 'required':
        return 'Argument is \033[1;95mrequired\033[0m and was not supplied';
    if state.kind == 'min-args':
        return 'Expected \033[1;95mat least\033[0m \033[1m{}\033[0m arguments. Recieved \033[1m{}\033[0m.'.format(state.expected, state.actual);
    if state.kind == 'max-args':
        return 'Expected \033[1;95mat most\033[0m \033[1m{}\033[0m arguments. Recieved \033[1m{}\033[0m.'.format(state.expected, state.actual);
    if state.kind == 'value':
        return 'Use of \033[1;95minvalid value\033[0m. See description of command for permissible values.';
    return '(Unknown)';
