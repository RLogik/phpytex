#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import random
import re
from collections import defaultdict
from typing import Any
from typing import Literal
from typing import TypeVar

from numpy.random import MT19937
from numpy.random import RandomState
from numpy.random import SeedSequence

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "inheritance_on_graph",
    "len_whitespace",
    "reseed",
    "size_of_whitespace",
    "unique",
]

# ----------------------------------------------------------------
# LOCAL VARIABLES
# ----------------------------------------------------------------

T = TypeVar("T")

# ----------------------------------------------------------------
# METHODS: string
# ----------------------------------------------------------------


def len_whitespace(
    text: str,
    /,
    *,
    mode: Literal[-1] | Literal[0] | Literal[1] = 0,
) -> int:
    r"""
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
    """
    n = 0
    match mode:
        case -1:
            text = re.sub(r"^(\s*).*$", r"\1", text)
        case 1:
            text = re.sub(r"^(|.*\S)(\s*)$", r"\2", text)

    for alpha in text:
        match alpha:
            case " ":
                n += 1
            case "\t":
                # go to next tab stop
                t = n // 8  # index of current tab-stop
                n = 8 * (t + 1)
    return n


def size_of_whitespace(
    text: str,
    /,
    *,
    indent: str,
) -> int:
    """
    Computes the whole number of indentations (roughly) equivalent to a given whitespace text.
    """
    n = len_whitespace(text)
    unit = len_whitespace(indent)
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


def inheritance_on_graph(
    edges: list[tuple[T, T]],
    hasProperty: dict[T, bool],
    /,
) -> defaultdict[T, bool]:
    """
    @inputs:
    - `edges` of a finite graph
    - an abstract `hasProperty` dictionary, assigning to each node, if property holds

    @returns:
    copy of `hasProperty` wherein all descendants of nodes with property have property

    TODO: replace this with method that uses networkx.
    """
    P: list[T] = []
    for u, value in hasProperty.items():
        if value:
            P.append(u)

    properties: defaultdict[T, bool] = defaultdict(lambda: False)
    properties.update(hasProperty)

    # keep updating until stable:
    while True:
        changed = False
        for u, v in edges:
            if u in P and v not in P:
                P.append(v)
                properties[v] = True
                changed = True

        if not changed:
            break

    return properties


# ----------------------------------------------------------------
# METHODS: maths
# ----------------------------------------------------------------


def reseed(
    seed: int | None,
    legacy: bool = False,
) -> RandomState:
    rng = RandomState(MT19937(SeedSequence(seed)))
    if legacy:
        random.seed(seed)
    return rng
