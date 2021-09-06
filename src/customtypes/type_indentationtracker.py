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
    pattern:   str;
    symb:      str;
    firstline:  bool;
    reference: int;
    start:     int;
    last:      int;

    def __init__(self, symb: str, pattern: str):
        self.symb = symb;
        self.pattern = pattern;
        self.reset();
        return;

    def reset(self):
        self.reference = 0;
        self.firstline = True;
        self.start     = 1;
        self.last      = 1;

    def size(self, s: str) -> int:
        # return len(re.findall(self.pattern, s));
        lenIndent = lengthOfWhiteSpace(s);
        lenUnit = lengthOfWhiteSpace(self.symb);
        return int(lenIndent / lenUnit);

    def relativeOffset(self, s: str):
        return max(self.size(s) - self.reference, 1);

    def initOffset(self, s: str) -> int:
        self.reset();
        self.reference = self.size(s);
        return self.reference;

    def setOffset(self, s: str) -> int:
        n = self.relativeOffset(s)
        if self.firstline:
            self.start = n;
            self.firstline = False;
        self.last = n;
        return self.last;

    def decrOffset(self) -> int:
        self.last = max(self.last - 1, 1);
        return self.last;

    def incrOffset(self) -> int:
        self.last = self.last + 1;
        return self.last;
