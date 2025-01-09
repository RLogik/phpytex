#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import re
import tokenize

from ..._core.utils.basic import *
from ..._core.utils.code import *
from ...models.enums import *
from .tokeniser import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "get_size_of_final_indentation",
    "get_size_of_first_indentation",
    "get_sizes_of_final_indentations",
]

# ----------------------------------------------------------------
# MAIN METHOD
# ----------------------------------------------------------------


@make_safe(default=0)
def get_size_of_first_indentation(
    *lines: str,
    indent: str = "    ",
    split_lines: bool = True,
) -> int:
    """
    Detects padding size of code block by inspecting the first line
    which does not consist purely of whitespace.

    This allows us to use interrupted blocks which start off with positive indents.
    """
    if split_lines:
        lines = ("\n".join(lines)).split("\n")

    line = next(filter(lambda x: len(x.rstrip()), lines), "")
    space = re.sub(r"^(\s*).*$", r"\1", line)
    pad = size_of_whitespace(space, indent=indent)
    return pad


@make_safe(default_factory=list)
def get_sizes_of_final_indentations(
    *lines: str,
    indent: str = "    ",
    split_lines: bool = True,
) -> list[int]:
    r"""
    Determines the final indentation levels in natural subsections of a block of code.

    ## Background ##

    Python's native tokeniser divides the code up into sections,
    ended by a `ENDMARKER` token.
    Before this token is reached a final `NEWLINE` token is given,
    followed a series of `DEDENT` tokens,
    which betray the final indentation level.

    ## Method ##

    This method therefore ignores all tokens, until this
    ```
    NEWLINE-DEDENT-DEDENT-...-DEDENT-ENDMARKER
    ```
    sequence occurs.

    Note:
    If a final line before the last `NEWLINE` ends in the `:`-operator
    (ignoring comments), then the final indentation level is treated as +1 its actual value.

    """
    if split_lines:
        lines = ("\n".join(lines)).split("\n")

    # first need to pad code to prevent parser from failing for interrupted blocks.
    pad = get_size_of_first_indentation(*lines, indent=indent, split_lines=False)
    pre = [f"{indent * i}def _():" for i in range(pad)]

    # cumulatively group together tokens and yield indentation:
    level = 0
    indents = []
    in_final_sequence = False
    last_token = None
    for token in tokenise_code(*pre, *lines):
        match token.type, in_final_sequence:
            case ((tokenize.NL | tokenize.NEWLINE), False):
                in_final_sequence = True
                level = 0
                continue

            case tokenize.DEDENT, True:
                level += 1
                continue

            case tokenize.ENDMARKER, True:
                # if last line before NL ended in ":" then bump the level!
                if (
                    last_token is not None
                    and last_token.type == tokenize.OP
                    and last_token.string == ":"
                ):
                    level += 1
                indents.append(level)

                # reset
                last_token = None
                in_final_sequence = False
                level = 0

            case _:
                # reset if necessary
                in_final_sequence = False
                level = 0

                # keep track of last token before next NL
                if token.type not in [
                    tokenize.NEWLINE,
                    tokenize.INDENT,
                    tokenize.DEDENT,
                    tokenize.ENDMARKER,
                    tokenize.COMMENT,
                ]:
                    last_token = token

    return indents


@make_safe_none
def get_size_of_final_indentation(
    *lines: str,
    indent: str = "    ",
) -> int | None:
    """
    Determines the final indentation level in a block of code.
    """
    indents = get_sizes_of_final_indentations(*lines, indent=indent)
    if len(indents) == 0:
        return None

    return indents[-1]
