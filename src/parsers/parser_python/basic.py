#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import re
import tokenize
from typing import Generator

from ..._core.utils.basic import *
from ...models.enums import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "get_full_indentation",
    "get_indentation_of_group",
    "get_padding",
    "group_ends_in_colon",
    "tokenise_code",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def tokenise_code(
    code: str,
    encoding: ENCODING = "utf-8",
) -> Generator[tokenize.TokenInfo, None, None]:
    """
    Method to tokenise code line by line
    """
    lines = iter(code.split("\n"))

    def stream() -> bytes:
        line = next(lines)
        return line.encode()

    return tokenize.tokenize(stream)


def group_ends_in_colon(tokengroup: list[tokenize.TokenInfo]) -> bool:
    """
    Detects if line ends in ':' (works even if line actually ends in comment or split )
    """
    if len(tokengroup) > 0:
        token = tokengroup[-1]
        return token.type == tokenize.OP and token.string == ":"
    return False


def get_indentation_of_group(tokengroup: list[tokenize.TokenInfo]):
    for token in tokengroup:
        if token.type in [tokenize.INDENT, tokenize.DEDENT]:
            line = token.line.rstrip()
            indent = get_full_indentation(token)
            return [] if line == "" else [indent]

    return []


def get_full_indentation(token: tokenize.TokenInfo) -> str:
    """
    NOTE: tokenize does not always compute the full indentation of INDENT/DEDENT tokens, so need to manually extract.
    """
    line = token.line.rstrip()
    indent = re.sub(r"^(\s*).*$", r"\1", line)
    return indent


def get_padding(
    codelines: list[str],
    indentsymb: str,
) -> int:
    """
    Detects padding size of code block by inspecting the first line
    which does not consist purely of whitespace.

    This allows us to use interrupted blocks which start off with positive indents.
    """
    try:
        line = next(filter(lambda x: len(x.rstrip()), codelines))
        indent = re.sub(r"^(\s*).*$", r"\1", line)
        pad = size_of_whitespace(indent, indentsymb=indentsymb)
        return pad

    except Exception as _:
        return 0
