#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from yaml import add_constructor;
from yaml import load;
from yaml import Loader;
from yaml import FullLoader;

from src.core.utils import getAttribute;
from src.config.customtypes import EvalType;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setupYamlReader():
    def not_constructor(loader: Loader, node) -> bool:
        value = loader.construct_sequence(node, deep=True);
        try:
            expr = not value[0];
        except:
            expr = False;
        return expr;

    def key_constructor(loader: Loader, node):
        value = loader.construct_sequence(node, deep=True);
        try:
            obj = value[0];
            keys = value[1:]
            return getAttribute(obj, *keys)
        except:
            return None;

    def join_constructor(loader: Loader, node):
        values = loader.construct_sequence(node, deep=True);
        try:
            sep   = str(values[0]);
            parts = [str(_) for _ in values[1]];
            # value = sep.join(parts);
            value = None;
            for part in parts:
                if value is None:
                    value = part;
                else:
                    value += sep + part;
            return value or '';
        except:
            return '';

    def eval_constructor(loader: Loader, node):
        value = loader.construct_sequence(node, deep=True);
        try:
            expr = value[0];
        except:
            expr = None;
        return EvalType(expr);

    add_constructor(u'!eval', eval_constructor);
    add_constructor(u'!not', not_constructor);
    add_constructor(u'!join', join_constructor);
    add_constructor(u'!key', key_constructor);
    return;

def readConfigFile(path: str) -> dict:
    with open(path, 'r') as fp:
        spec = load(fp, Loader=FullLoader);
        if not isinstance(spec, dict):
            raise ValueError('Config is not a dictionary object!');
    return spec;
