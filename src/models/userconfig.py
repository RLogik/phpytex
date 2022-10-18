#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.config import *;

from src.core.utils import getAttribute;
from src.customtypes.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setupYamlReader():
    def not_constructor(loader: yaml_Loader, node) -> bool:
        value = loader.construct_sequence(node, deep=True);
        try:
            expr = not value[0];
        except:
            expr = False;
        return expr;

    def key_constructor(loader: yaml_Loader, node):
        value = loader.construct_sequence(node, deep=True);
        try:
            obj = value[0];
            keys = value[1:]
            return getAttribute(obj, *keys)
        except:
            return None;

    def join_constructor(loader: yaml_Loader, node):
        values = loader.construct_sequence(node, deep=True);
        try:
            sep, parts = str(values[0]), [str(_) for _ in values[1]];
            return sep.join(parts);
        except:
            return '';

    def eval_constructor(loader: yaml_Loader, node):
        value = loader.construct_sequence(node, deep=True);
        try:
            expr = value[0];
        except:
            expr = None;
        return EvalType(expr);

    add_constructor(tag=u'!eval', constructor=eval_constructor);
    add_constructor(tag=u'!not',  constructor=not_constructor);
    add_constructor(tag=u'!join', constructor=join_constructor);
    add_constructor(tag=u'!key',  constructor=key_constructor);
    return;
