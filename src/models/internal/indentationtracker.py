#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.thirdparty.types import *;
from src.core.utils import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'IndentationTracker',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS indentation tracker
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IndentationTracker(object):
    pattern: str;
    symbol: str;
    reference: tuple[int, int];
    level: int;

    def __init__(
        self,
        symbol: str,
        pattern: str,
        reference: str = ''
    ):
        self.symbol = symbol;
        self.pattern = pattern;
        self.level = 0;
        self.reference = size_of_indent(reference, unit=symbol);
        return;

    def _compute_offset(self, s: str) -> int:
        # compute size of
        n0, r0 = self.reference;
        n, r = size_of_indent(s, unit=self.symbol);
        return max(n - n0, 0);

    def set_offset(self, s: str):
        '''
        Computes the level of indentation based on string `s`
        computed relative to the indentation symbol.
        '''
        self.level = self._compute_offset(s);
        return;

    def __iadd__(self, n: Any):
        '''
        Increase indentation by `n` levels.
        '''
        if not isinstance(n, int):
            raise Exception(f'Can only perfor {self} += <int>-type!');
        if n < 0:
            return self.__isub__(-n);
        self.level += 1;
        return self.level;

    def __isub__(self, n: Any):
        '''
        Decrease indentation by `n` levels.
        '''
        if not isinstance(n, int):
            raise Exception(f'Can only perfor {self} += <int>-type!');
        if n < 0:
            return self.__iadd__(-n);
        self.level = max(self.level - 1, 0);
        return self.level;
