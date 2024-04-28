#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ..thirdparty.misc import *
from ..thirdparty.system import *
from ..thirdparty.types import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'len_whitespace',
    'size_of_whitespace',
    'unique',
    'inheritanceOnGraph',
]

# ----------------------------------------------------------------
# LOCAL VARIABLES
# ----------------------------------------------------------------

T = TypeVar('T')

# ----------------------------------------------------------------
# METHODS: string
# ----------------------------------------------------------------


def len_whitespace(
    text: str,
    mode: Literal[-1] | Literal[0] | Literal[1] = 0,
) -> int:
    '''
    Computes the effective length of white-space occuring in text as follows:

    - spaces count as `1`.
    - tab count as moving the position to the next tab-stop,
      which occur at wholenumber multiples of `8`.

    - If `mode = 0` - considers all white space.
    - If `mode = -1` - considers only white spaces left of
        the first occurrence of non-whitespace characters (if any).
    - If `mode = 1` - considers only white spaces right of
        the final occurrence of non-whitespace characters (if any).

    ## Examples ##

    ```py
    len_whitespace(' ') # 1
    len_whitespace('  ') # 2
    len_whitespace('\\t') # 8
    len_whitespace(' \\t') # 8
    len_whitespace('  \\t') # 8
    len_whitespace('\\t   ') # 11
    len_whitespace(' \\t') # 11
    len_whitespace('  \\t   ') # 11
    ```
    '''
    n = 0
    match mode:
        case -1:
            text = re.sub(r'^(\s*).*$', r'\1', text)
        case 1:
            text = re.sub(r'^(|.*\S)(\s*)$', r'\2', text)
    for alpha in text:
        match alpha:
            case ' ':
                n += 1
            case '\t':
                # go to next tab stop
                t = n // 8  # index of current tab-stop
                n = 8 * (t + 1)
    return n


def size_of_whitespace(text: str, indentsymb: str) -> int:
    '''
    Computes the whole number of indentations (roughly) equivalent to a given whitespace text.
    '''
    n = len_whitespace(text)
    unit = len_whitespace(indentsymb)
    return n // unit


# ----------------------------------------------------------------
# METHODS: array methods
# ----------------------------------------------------------------


def unique(X: list[Any]) -> list[Any]:
    X_ = []
    for el in X:
        if el in X_:
            continue
        X_.append(el)
    return X_


# ----------------------------------------------------------------
# METHODS: inheritance properties on graphs
# ----------------------------------------------------------------


def inheritanceOnGraph(edges: list[tuple[str, str]], hasProperty: dict[str, bool]):
    '''
    @inputs:
    - `edges` of a finite graph
    - an abstract `hasProperty` dictionary, assigning to each node, if property holds

    @returns:
    copy of `hasProperty` wherein all descendants of nodes with property have property

    TODO: replace this with method that uses networkx.
    '''
    P = []
    for u, value in hasProperty.items():
        if value:
            P.append(u)
    properties = {u: value for u, value in hasProperty.items()}
    for u, v in edges:
        if not (u in properties):
            properties[u] = False
        if not (v in properties):
            properties[v] = False
    # keep updating until stable:
    while True:
        changed = False
        for u, v in edges:
            if u in P and not (v in P):
                P.append(v)
                properties[v] = True
                changed = True
        if not changed:
            break
    return properties
