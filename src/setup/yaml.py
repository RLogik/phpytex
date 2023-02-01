#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.config import *;

from src.models.internal import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS / LOCAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constructors
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@yaml_add_constructor(tag=u'!not', attach=True)
def constructor(loader: YamlLoader, node: YamlSequenceNode) -> bool:
    value = loader.construct_sequence(node, deep=True);
    try:
        return not bool(value[0]);
    except:
        pass;
    return False;

@yaml_add_constructor(tag=u'!key', attach=True)
def constructor(loader: YamlLoader, node: YamlSequenceNode):
    value = loader.construct_sequence(node, deep=True);
    try:
        obj = value[0];
        keys = value[1:];
        while len(keys) > 0 and isinstance(obj, dict):
            key, keys = keys[0], keys[1:];
            obj = obj.get(key, None);
        if isinstance(obj, dict):
            return obj;
    except:
        pass;
    return None;

@yaml_add_constructor(tag=u'!join', attach=True)
def constructorn(loader: YamlLoader, node: YamlSequenceNode):
    values = loader.construct_sequence(node, deep=True);
    try:
        sep, parts = str(values[0]), [str(_) for _ in values[1]];
        return sep.join(parts);
    except:
        pass;
    return '';

@yaml_add_constructor(tag=u'!eval', attach=True)
def constructorl(loader: YamlLoader, node: YamlSequenceNode):
    value = loader.construct_sequence(node, deep=True);
    try:
        return EvalType(str(value[0]));
    except:
        pass;
    return EvalType();

@yaml_add_constructor(tag=u'!tuple', attach=True)
def constructorle(loader: YamlLoader, node: YamlSequenceNode):
    value = loader.construct_sequence(node, deep=True);
    try:
        return tuple(value);
    except:
        pass;
    return None;
