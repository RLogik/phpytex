#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from yaml import add_constructor;
from yaml import load;
from yaml import Loader;
from yaml import FullLoader;

from src.core.utils import getAttribute;
from src.customtypes.exports import *;

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
            sep, parts = str(values[0]), [str(_) for _ in values[1]];
            return sep.join(parts);
        except:
            return '';

    def eval_constructor(loader: Loader, node):
        value = loader.construct_sequence(node, deep=True);
        try:
            expr = value[0];
        except:
            expr = None;
        return EvalType(expr);

    add_constructor(tag=u'!eval', constructor=eval_constructor, Loader=Loader);
    add_constructor(tag=u'!not',  constructor=not_constructor,  Loader=Loader);
    add_constructor(tag=u'!join', constructor=join_constructor, Loader=Loader);
    add_constructor(tag=u'!key',  constructor=key_constructor,  Loader=Loader);
    return;

def readYamlFile(path: str) -> dict:
    with open(path, 'r') as fp:
        spec = load(fp, Loader=FullLoader);
        if not isinstance(spec, dict):
            raise ValueError('Config is not a dictionary object!');
    return spec;
