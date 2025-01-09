#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from ..._core.utils.basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "IndentationTracker",
]

# ----------------------------------------------------------------
# CLASS indentation tracker
# ----------------------------------------------------------------


class IndentationTracker(BaseModel):
    """
    A helper class to keep track of indentation level.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    symb: str
    reference: str = Field(default="")
    level: int = Field(default=0)
    reference_level: int = Field(default=0, init=False)

    def model_post_init(self, __context):
        self.reference_level = size_of_whitespace(
            self.reference,
            indent=self.symb,
        )

    def compute_relative_offset(
        self,
        s: str,
        /,
    ) -> int:
        n0 = self.reference_level
        n = size_of_whitespace(s, indent=self.symb)
        return max(n - n0, 0)

    def set_offset(
        self,
        x: str | int,
        /,
    ):
        match x:
            case int():
                self.level = x

            case _:
                # case str():
                self.level = self.compute_relative_offset(x)

    def decr_offset(self) -> int:
        self.level = max(self.level - 1, 0)
        return self.level

    def incr_offset(self) -> int:
        self.level += 1
        return self.level
