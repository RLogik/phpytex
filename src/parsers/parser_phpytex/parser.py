#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging

from ..._core.logging import *
from ...models.enums import *
from ...models.transpilation import *
from ...thirdparty.config import *
from ...thirdparty.types import *
from ..parser_python import *
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
    indentation: IndentationTracker,
    offset: str = "",
) -> Generator[TranspileBlock, None, None]:
    if text.strip() == "":
        return

    try:
        tokeniser = Tokeniser()
        u = tokeniser.parse("blocks", text)
        yield from lexed_to_blocks(tokeniser, u, offset=offset, indentation=indentation)

    except Exception as err:
        logging.error(err)
        yield from lexed_to_block_feed(tokeniser, text, offset=offset, indentation=indentation)
