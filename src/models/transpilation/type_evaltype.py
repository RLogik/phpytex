#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "EvalType",
]

# ----------------------------------------------------------------
# CLASS EvalType for usage with yaml
# ----------------------------------------------------------------


class EvalType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )

    expr: str = Field(default_factory=lambda: str(None))

    def __str__(self) -> str:
        return self.expr
