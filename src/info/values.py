#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import List;
from typing import Union;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Value
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Value:
    values: List[Union[None, bool, str, int, float]];
    value: Union[None, bool, str, int, float];
    default: Union[None, bool, str, int, float];
    valid: bool = True;

    def __init__(self, values=[], value=None, default=None, valid=True, **kwargs):
        self.values = values;
        self.value = value;
        self.default = default;
        self.valid = valid;

    def __iter__(self):
        for _ in self.values:
            yield _;

    def __len__(self) -> int:
        return len(self.values);

    def __str__(self):
        return str(self.value);
