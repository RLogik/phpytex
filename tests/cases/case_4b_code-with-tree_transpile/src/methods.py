#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from typing import Generator

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "generate_definitions",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def generate_definitions() -> Generator[tuple[str | None, str], None, None]:
    yield "Vec0", r"\ket{0}"
    yield "Vec1", r"\ket{1}"
    yield None, "should be ignored"
    yield "Proj0", r"\ket{0}\bra{0}"
    yield "Proj1", r"\ket{0}\bra{1}"
