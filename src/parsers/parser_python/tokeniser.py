#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import tokenize
from typing import Generator

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "tokenise_code",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def tokenise_code(
    *lines: str,
    all_blocks: bool = True,
) -> Generator[tokenize.TokenInfo, None, None]:
    """
    Uses python's native tokeniser to tokenise a block of code.
    """
    prev = None  # stores a "peeked" line
    stream = iter(lines)

    # bytes-generator to stream the contents
    def reader() -> bytes:
        nonlocal prev
        line = prev or next(stream)
        prev = None
        return line.encode()

    # Keep scanning until all lines read.
    # NOTE: the tokeniser stops at empty lines
    # so need to constantly "peek" to see if stream is not finished.
    while True:
        yield from tokenize.tokenize(reader)
        if not all_blocks:
            break

        try:
            prev = next(stream)

        except StopIteration as _:
            break
