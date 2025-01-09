#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
from typing import Generator

from ...models.transpilation import *
from .parts import *
from .tokeniser import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "parse",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def parse(
    text: str,
    /,
    *,
    tokeniser: Tokeniser,
    indentation: IndentationTracker,
    offset: str = "",
) -> Generator[TranspileBlock, None, None]:
    if text.strip() == "":
        return

    try:
        u = tokeniser.parse(text, mode="blocks")
        yield from lexed_to_blocks(tokeniser, u, offset=offset, indentation=indentation)

    except Exception as err:
        logging.error(err)
        yield from lexed_to_block_feed(tokeniser, text, offset=offset, indentation=indentation)
