#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...thirdparty.types import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'EvalType',
]

# ----------------------------------------------------------------
# CLASS EvalType for usage with yaml
# ----------------------------------------------------------------


class EvalMetaType(type):
    __name__ = 'evaluation'

    @classmethod
    def __instancecheck__(cls, o) -> bool:
        try:
            return type(o).__name__ == cls.__name__
        except:
            return False


class EvalType(metaclass=EvalMetaType):
    _expr: str = str(None)

    def __init__(self, expr):
        if isinstance(expr, str):
            self._expr = expr
        return

    @property
    def expr(self):
        return self._expr

    def __str__(self) -> str:
        return self.expr
