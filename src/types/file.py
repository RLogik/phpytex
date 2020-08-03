#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class/Type: FileType
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileTypeMeta(type):
    __name__ = 'file';

    @classmethod
    def __instancecheck__(cls, o) -> bool:
        try:
            return isinstance(o, str) and os.path.isfile(o);
        except:
            return False;

class FileType(metaclass=FileTypeMeta):
    __value: str;

    def __init__(self, value=None, *arg, **kwargs):
        if isinstance(value, str):
            self.__value = value;

    def __str__(self) -> str:
        if not hasattr(self, '__value'):
            raise ValueError('No value set.');
        return self.__value;
