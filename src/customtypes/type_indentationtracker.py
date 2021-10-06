#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.core.utils import lengthOfWhiteSpace;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS indentation tracker
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IndentationTracker(object):
    pattern:    str;
    symb:       str;
    _reference: int;
    level:     int;

    def __init__(
        self,
        symb: str,
        pattern: str
    ):
        self.symb = symb;
        self.pattern = pattern;
        self.initOffset();
        return;

    def size(self, s: str) -> int:
        lenIndent = lengthOfWhiteSpace(s);
        lenUnit = lengthOfWhiteSpace(self.symb);
        return int(lenIndent / lenUnit);

    def relativeOffset(self, s: str):
        return max(self.size(s) - self._reference, 0);

    def initOffset(self, s: str = '') -> int:
        self.level      = 0;
        self._reference = self.size(s);
        return self._reference;

    def setOffset(self, s: str) -> int:
        n = self.relativeOffset(s);
        self.level = n;
        return self.level;

    def decrOffset(self) -> int:
        self.level = max(self.level - 1, 0);
        return self.level;

    def incrOffset(self) -> int:
        self.level += 1;
        return self.level;
