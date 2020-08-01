#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import List;
from typing import Union;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Key
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Key:
    names: List[str];

    def __init__(self, obj: Union[str, List[str]] = []):
        if isinstance(obj, list):
            self.names = obj;
        else:
            self.names = [obj];

    def __iter__(self):
        for _ in self.names:
            yield _;

    def __len__(self) -> int:
        return len(self.names);

    def __str__(self):
        return str(self.name);

    def __eq__(self, other: str):
        return other in self.names;

    @property
    def name(self) -> str:
        if len(self.names) == 0:
            raise ValueError('No key set!');
        return self.names[0];
