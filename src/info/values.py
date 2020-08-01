#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import List;
from typing import Union;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Values
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Value:
    values: Union[None, bool, str, int, float, List[Union[None, bool, str, int, float]]];
    value: Union[None, bool, str, int, float];
    default: Union[None, bool, str, int, float];

    def __init__(self, values=None, value=None, default=None, **kwargs):
        self.values = values;
        self.value = value;
        self.default = default;

    def __str__(self):
        return str(self.value);
