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
    is_legacy: bool;

    pattern:   str;
    symb:      str;
    firstline: bool;
    reference: int;
    start:     int;
    last:      int;

    def __init__(
        self,
        symb: str,
        pattern: str,
        is_legacy: bool = False
    ):
        self.is_legacy = is_legacy;
        self.symb = symb;
        self.pattern = pattern;
        self.initOffset();
        return;

    # def resetOffset(self):
    #     if self.legacy:
    #     else:
    #     return;

    def size(self, s: str) -> int:
        # return len(re.findall(self.pattern, s));
        lenIndent = lengthOfWhiteSpace(s);
        lenUnit = lengthOfWhiteSpace(self.symb);
        return int(lenIndent / lenUnit);

    def relativeOffset(self, s: str):
        return max(self.size(s) - self.reference, 0);

    def initOffset(self, s: str = '') -> int:
        self.firstline = True;
        self.start     = 0;
        self.last      = 0;
        self.reference = self.size(s) + (1 if self.is_legacy else 0);
        return self.reference;

    def setOffset(self, s: str) -> int:
        n = self.relativeOffset(s);
        self.start = n if self.firstline else self.start;
        self.last = n;
        self.firstline = False;
        return self.last;

    def decrOffset(self) -> int:
        self.last = max(self.last - 1, 0);
        return self.last;

    def incrOffset(self) -> int:
        self.last += 1;
        return self.last;
