#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.config import *;
from src.local.maths import *;

from src.core.utils import getAttribute;
from src.customtypes.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setupYamlReader():
    def include_constructor(loader: yaml.Loader, node: yaml.Node):
        try:
            value = loader.construct_yaml_str(node);
            assert isinstance(value, str);
            args = value.split(r'/#/');
            path, keys_as_str = (args + [''])[:2]
            with open(path, 'r') as fp:
                obj = yaml.load(fp, Loader=yaml.FullLoader);
            keys = keys_as_str.split('/')
            for key in keys:
                if key != '':
                    obj = obj[key];
            return obj;
        except:
            return None;

    def not_constructor(loader: yaml.Loader, node: yaml.Node) -> bool:
        try:
            value = loader.construct_yaml_bool(node);
            return not value;
        except:
            return None;

    def key_constructor(loader: yaml.Loader, node: yaml.Node):
        try:
            value = loader.construct_sequence(node, deep=True);
            obj = value[0];
            keys = value[1:]
            return getAttribute(obj, *keys)
        except:
            return None;

    def join_constructor(loader: yaml.Loader, node: yaml.Node):
        try:
            values = loader.construct_sequence(node, deep=True);
            sep, parts = str(values[0]), [str(_) for _ in values[1]];
            return sep.join(parts);
        except:
            return '';

    def eval_constructor(loader: yaml.Loader, node: yaml.Node):
        try:
            value = loader.construct_sequence(node, deep=True);
            expr = value[0];
        except:
            expr = None;
        return EvalType(expr);

    def tuple_constructor(loader: yaml.Loader, node: yaml.Node):
        try:
            value = loader.construct_sequence(node, deep=True);
            return tuple(value);
        except:
            return None;

    def fraction_constructor(loader: yaml.Loader, node: yaml.Node):
        try:
            value = loader.construct_yaml_str(node);
            return Fraction(value);
        except:
            return None;

    yaml.add_constructor(tag=u'!include', constructor=include_constructor);
    yaml.add_constructor(tag=u'!eval', constructor=eval_constructor);
    yaml.add_constructor(tag=u'!not', constructor=not_constructor);
    yaml.add_constructor(tag=u'!join', constructor=join_constructor);
    yaml.add_constructor(tag=u'!key', constructor=key_constructor);
    yaml.add_constructor(tag=u'!tuple', constructor=tuple_constructor);
    yaml.add_constructor(tag=u'!fraction', constructor=fraction_constructor);
    return;
