#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import json
from typing import Any

from lark import Tree

from ....models.transpilation import *
from ..tokeniser import *
from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "process_arg_list",
    "process_block_code_arguments",
    "process_code_inline",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def process_code_inline(
    u: Tree,
    indentation: IndentationTracker,
) -> TranspileBlock:
    children = filter_subexpr(u)
    indent = indentation.symb * indentation.level
    match u.data:
        case "codeinline":
            return process_code_inline(children[0], indentation=indentation)
        case "codeoneline":
            lines = format_value([lexed_to_str(u)], indent=indent)
            return TranspileBlock(
                kind="code:value",
                lines=lines,
                level=indentation.level,
                indentsymb=indentation.symb,
            )
        case "codemultiline":
            lines = format_value([lexed_to_str(child) for child in children], indent=indent)
            return TranspileBlock(
                kind="code:value",
                lines=lines,
                level=indentation.level,
                indentsymb=indentation.symb,
            )
    raise Exception("Could not parse expression!")


def process_block_code_arguments(u: Tree) -> tuple[list[str], dict[str, Any]]:
    typ = u.data
    children = filter_subexpr(u)
    if typ == "blockcode_args":
        return process_arg_list(children[0])
    raise Exception("Could not parse expression!")


def process_arg_list(u: Tree) -> tuple[list[str], dict[str, Any]]:
    typ = u.data
    children = filter_subexpr(u)
    if typ == "arglist":
        tokens = []
        kwargs = dict()
        for child in children:
            while isinstance(child, Tree) and child.data not in [
                "argoption_token",
                "argoption_kwarg",
            ]:
                child = child.children[0]
            grandchildren = filter_subexpr(child)
            if child.data == "argoption_kwarg":
                key = lexed_to_str(grandchildren[0])
                value = lexed_to_str(grandchildren[1])
                try:
                    value = json.loads(value)
                except Exception:
                    pass
                kwargs[key] = value
            elif child.data == "argoption_token":
                value = lexed_to_str(grandchildren[0])
                tokens.append(value)
        return tokens, kwargs
    raise Exception("Could not parse expression!")
