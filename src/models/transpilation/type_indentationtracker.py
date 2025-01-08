#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

from ..._core.utils.basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'IndentationTracker',
]

# ----------------------------------------------------------------
# CLASS indentation tracker
# ----------------------------------------------------------------


class IndentationTracker(object):
    pattern: str
    symb: str
    reference: int
    level: int

    def __init__(self, symb: str, pattern: str, reference: str = ''):
        self.symb = symb
        self.pattern = pattern
        self.level = 0
        self.reference = size_of_whitespace(reference, indentsymb=symb)
        return

    def relativeOffset(self, s: str):
        return max(size_of_whitespace(s, indentsymb=self.symb) - self.reference, 0)

    def setOffset(self, s: str) -> int:
        n = self.relativeOffset(s)
        self.level = n
        return self.level

    def decrOffset(self) -> int:
        self.level = max(self.level - 1, 0)
        return self.level

    def incrOffset(self) -> int:
        self.level += 1
        return self.level
