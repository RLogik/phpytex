#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

import re;
from typing import Any;

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
        self.start     = 1;
        self.last      = 1;

    def computeIndentations(self, s: str, pattern = None) -> int:
        pattern = pattern if isinstance(pattern, str) else self.pattern;
        return len(re.findall(pattern, s));

    def initOffset(self, s: str):
        self.reset();
        self.reference = self.computeIndentations(s) + 1;

    def computeOffset(self, s: str):
        return max(self.computeIndentations(s) - self.reference, 1);

    def setOffset(self, s: str):
        self.last = self.computeOffset(s);

    def decrOffset(self):
        self.last = max(self.last - 1, 1);

    def incrOffset(self):
        self.last = self.last + 1;
