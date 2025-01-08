#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from typing import Generator

from lark import Tree

from ....models.transpilation import *
from ..tokeniser import *
from .basic import *
from .lexer_quick import *
from .process_block import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "lexed_to_block",
    "lexed_to_blocks",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def lexed_to_blocks(
    tokeniser: Tokeniser,
    u: Tree,
    offset: str,
    indentation: IndentationTracker,
) -> Generator[TranspileBlock, None, None]:
    children = filter_subexpr(u)
    match u.data:
        case "blocks":
            for child in children:
                yield lexed_to_block(tokeniser, child, offset=offset, indentation=indentation)
            return

        case _ as t:
            raise Exception(f"Could not parse {t} expression!")


def lexed_to_block(
    tokeniser: Tokeniser,
    u: Tree,
    offset: str,
    indentation: IndentationTracker,
) -> TranspileBlock:
    children = filter_subexpr(u)
    match u.data:
        case "blockfeedone" | "block" | "blockcomment":
            return lexed_to_block(
                tokeniser, children[0], offset=offset, indentation=indentation
            )

        case "emptyline":
            return TranspileBlock(
                kind="text:empty",
                level=indentation.level,
                indentsymb=indentation.symb,
            )

        case "blockcomment_simple":
            return TranspileBlock(
                kind="text:comment",
                content=lexed_to_str(u),
                level=indentation.level,
                indentsymb=indentation.symb,
                parameters=TranspileBlockParameters(keep=False),
            )

        case "blockcomment_keep":
            return TranspileBlock(
                kind="text:comment",
                content=lexed_to_str(u),
                level=indentation.level,
                indentsymb=indentation.symb,
                parameters=TranspileBlockParameters(keep=True),
            )

        # TEXT CONTENT
        case "blockcontent":
            # attempt to re-process as quick command:
            try:
                text = lexed_to_str(u)
                u = tokeniser.parse(text, mode="blockquick")
                return lexed_to_quick_block(u, indentation=indentation)

            # otherwise, consider block to contain purely text + inline code:
            except Exception:
                return process_block_content(children, indentation=indentation)

        # CODE BLOCK REGEX
        case "blockcode_regex":
            text = lexed_to_str(u)
            return process_block_code_regex(
                tokeniser,
                text,
                offset=offset,
                indentation=indentation,
            )

        # CODE BLOCK
        case "blockcode":
            return process_block_code(children[0], offset=offset, indentation=indentation)

    raise Exception("Could not parse expression!")
