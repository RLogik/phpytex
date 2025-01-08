#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import re
from fractions import Fraction

import yaml

from ...models.internal import *
from ...models.transpilation import *
from .code import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "register_yaml_constructors",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS
# ----------------------------------------------------------------

_yaml_constructors_registered = TriggerProperty()

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def register_yaml_constructors():
    """
    Registers yaml-sugar to help parse .yaml files
    """
    global _yaml_constructors_registered

    if _yaml_constructors_registered.value:
        return

    yaml.add_constructor(tag="!include", constructor=include_constructor)
    yaml.add_constructor(tag="!not", constructor=not_constructor)
    yaml.add_constructor(tag="!join", constructor=join_constructor)
    yaml.add_constructor(tag="!tuple", constructor=tuple_constructor)

    yaml.add_constructor(tag="!key", constructor=key_constructor)
    yaml.add_constructor(tag="!eval", constructor=eval_constructor)
    yaml.add_constructor(tag="!fraction", constructor=fraction_constructor)

    _yaml_constructors_registered.set()
    return


# ----------------------------------------------------------------
# PARTS
# ----------------------------------------------------------------


@make_safe_none
def include_constructor(loader: yaml.Loader, node: yaml.Node):
    value = loader.construct_yaml_str(node)
    assert isinstance(value, str)
    # parse argument
    m = re.match(pattern=r"^(.*)\/#\/?(.*)$", string=value)
    # read yaml from path
    path = m.group(1) if m else value
    register_yaml_constructors()
    with open(path, "rb") as fp:
        obj = yaml.load(fp, yaml.FullLoader)
    # get part of yaml
    keys_as_str = m.group(2) if m else ""
    keys = keys_as_str.split("/")
    for key in keys:
        if key == "":
            continue
        obj = obj.get(key, dict())

    return obj


@make_safe_none
def not_constructor(loader: yaml.Loader, node: yaml.Node) -> bool:
    value = loader.construct_yaml_bool(node)
    return not value


@make_safe(default="")
def join_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
    values = loader.construct_sequence(node, deep=True)
    sep, parts = str(values[0]), [str(_) for _ in values[1]]
    return sep.join(parts)


@make_safe_none
def tuple_constructor(loader: yaml.Loader, node: yaml.Node) -> tuple:
    value = loader.construct_sequence(node, deep=True)
    return tuple(value)


@make_safe_none
def key_constructor(loader: yaml.Loader, node: yaml.Node):
    value = loader.construct_sequence(node, deep=True)
    result = value[0]
    keys = value[1:]
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key, None)

        elif isinstance(key, int) and isinstance(result, (list, tuple)):
            result = result[key] if key < len(result) else None

        else:
            raise ValueError(f"Could not extract { '-> '.join(keys)} from {value[0]}")

    return result


@make_safe(default_factory=lambda: EvalType())
def eval_constructor(loader: yaml.Loader, node: yaml.Node) -> EvalType:
    value = loader.construct_sequence(node, deep=True)
    expr = value[0]
    assert isinstance(expr, str)
    return EvalType(expr)


@make_safe_none
def fraction_constructor(loader: yaml.Loader, node: yaml.Node) -> Fraction:
    value = loader.construct_yaml_str(node)
    return Fraction(value)
