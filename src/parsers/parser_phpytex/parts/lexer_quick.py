#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from lark import Tree

from ....models.transpilation import *
from ..tokeniser import *
from .basic import *
from .process_quick import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "lexed_to_quick_block",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def lexed_to_quick_block(
    u: Tree,
    indentation: IndentationTracker,
) -> TranspileBlock:
    children = filter_subexpr(u)
    match u.data:
        case "blockquick":
            textindent = lexed_to_str(children[0])
            return process_block_quick_command(
                children[1],
                textindent=textindent,
                indentation=indentation,
            )

    raise Exception("Could not parse expression!")
