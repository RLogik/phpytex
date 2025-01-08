#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ....thirdparty.lexers import *
from ....thirdparty.misc import *

from ...._core.utils.basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'rstrip_code',
    'lexed_to_str',
    'filter_subexpr',
    'filter_out_type_noncapture',
    'format_value',
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def rstrip_code(expr: str) -> str:
    return re.sub(r'[\s;]*$', '', expr)


def lexed_to_str(u: str | Tree) -> str:
    return u if isinstance(u, str) else ''.join([lexed_to_str(uu) for uu in u.children])


def filter_subexpr(u: Tree) -> list[Tree]:
    '''
    Filters for children which are trees and of 'noncapture' type.
    '''
    return [uu for uu in u.children if isinstance(uu, Tree) and filter_out_type_noncapture(uu)]


def filter_out_type_noncapture(u: Tree):
    return not (u.data == 'noncapture' or re.match(r'[A-Z]', u.data))


def format_value(lines: list[str], indent: str) -> list[str]:
    if len(lines) == 0:
        return []
    lines = unindent_lines(lines, reference=indent)
    lines[-1] = rstrip_code(lines[-1])
    return lines
