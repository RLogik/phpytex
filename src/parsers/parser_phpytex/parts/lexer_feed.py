#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import re
from typing import Generator

from ...._core.logging import *
from ....models.transpilation import *
from ..tokeniser import *
from .basic import *
from .lexer_block import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "lexed_to_block_feed",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def lexed_to_block_feed(
    tokeniser: Tokeniser,
    text: str,
    offset: str,
    indentation: IndentationTracker,
) -> Generator[TranspileBlock, None, None]:
    """
    NOTE: As this method is too slow.
    Thus only used when main parse-method fails,
    in order to pinpoint failure.
    """
    lines = re.split(r"\r?\n", text)
    numlines = len(lines)
    linespos = 0
    textrest = text

    while textrest != "":
        # attempt to lex next block:
        try:
            u = tokeniser.parse("blockfeed", textrest)

        except Exception as err:
            err.add_note(lex_error(lines, linespos))
            raise err

        # extract tokenised information:
        linespos_old = linespos
        children = filter_subexpr(u)
        if len(children) > 1:
            textrest = lexed_to_str(children[1])
            # NOTE: add character to ensure last line is not empty in line count:
            numlines_ = len(re.split(r"\r?\n", textrest + "."))
            linespos = numlines - numlines_

        # attempt to parse next block:
        try:
            yield lexed_to_block(tokeniser, children[0], offset=offset, indentation=indentation)

        except Exception as err:
            err.add_note(parse_error(lines, linespos_old, linespos))
            raise err

        # break, if no 'rest' found
        # TODO: should this be <= ?
        if len(children) == 1:
            break


# ----------------------------------------------------------------
# AUXILIARY METHODS
# ----------------------------------------------------------------


def lex_error(lines: list[str], linepos: int) -> str:
    text_consumed = lines[:linepos]
    text_remaining = lines[linepos:]
    messages = []

    # NOTE: display linepos + 1, as documents start with 1 not 0
    messages.append(
        f"At line \033[1m{linepos + 1}\033[0m the text could not be \033[1mtokenised\033[0m:"
    )
    messages.append("\033[1m--------------------------------\033[0m")
    messages += [f"\033[2m{line}\033[0m" for line in text_consumed[-3:]]
    messages += [f"\033[91;1m{line}\033[0m" for line in text_remaining[:1]]
    messages += [f"\033[2m{line}\033[0m" for line in text_remaining[1:3]]
    messages.append("\033[1m--------------------------------\033[0m")
    return "\n".join(messages)


def parse_error(lines: list[str], linepos1: int, linepos2: int) -> str:
    text_consumed = lines[:linepos1]
    text_block = lines[linepos1:linepos2]
    text_remaining = lines[linepos2:]
    messages = []

    # NOTE: display linepos + 1, as documents start with 1 not 0
    messages.append(
        f"At lines \033[1m{linepos1 + 1}\033[0m-\033[1m{linepos2 + 1}\033[0m the text could not be \033[1mparsed\033[0m:"
    )
    messages.append("\033[1m--------------------------------\033[0m")
    messages += [f"\033[2m{line}\033[0m" for line in text_consumed[-3:]]
    messages += [f"\033[91;1m{line}\033[0m" for line in text_block]
    messages += [f"\033[2m{line}\033[0m" for line in text_remaining[:3]]
    messages.append("\033[1m--------------------------------\033[0m")
    return "\n".join(messages)
