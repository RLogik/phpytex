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
    yield "VecZero", r"\ket{0}"
    yield "VecOne", r"\ket{1}"
    yield None, "should be ignored"
    yield "ProjZero", r"\ket{0}\bra{0}"
    yield "ProjOne", r"\ket{0}\bra{1}"
