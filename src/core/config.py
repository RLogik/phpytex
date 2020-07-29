#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from yaml import load;
from yaml import FullLoader;
from copy import deepcopy;
from typing import Any;
from typing import Dict;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def extractConfig(fname: str) -> Dict[str, Any]:
    try:
        with open(fname, 'r') as fp:
            struct = load(fp, Loader=FullLoader);
    except:
        struct = dict();
    return struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Decorator: @transfer_config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def transfer_config(cls):
    '''
    Transfers dictionary like attributes to a class
    '''

    def __init__(self, *args, **kwargs):
        for key in kwargs:
            if hasattr(cls, key):
                value = deepcopy(kwargs[key]);
                setattr(cls, key, value);

    cls.__init__ = __init__;
    return cls;
