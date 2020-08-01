#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import List;
from typing import Union;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: MultiValue
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MultiValue:
    items: List[Union[None, bool, str, int, float]];
    default: Union[None, bool, str, int, float];
    valid: bool;

    def __init__(self, items=[], item=None, default=None, valid=True, **kwargs):
        if not item is None:
            self.items = [item];
        else:
            self.items = items[:];
        self.default = default;
        self.valid = valid;

    def __iter__(self):
        for _ in self.items:
            yield _;

    def __len__(self) -> int:
        return len(self.items);

    def __str__(self):
        return str(self.items);

    def __eq__(self, other):
        value = self.value;
        if value is None and other is None:
            return True;
        elif value is None or other is None:
            return False;
        return value == other;

    @property
    def value(self):
        if len(self.items) > 0:
            return self.items[0];
        return self.default;

    @property
    def values(self):
        return self.items;
