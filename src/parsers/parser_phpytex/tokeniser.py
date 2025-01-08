#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...setup import *
from ...thirdparty.code import *
from ...thirdparty.lexers import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "Tokeniser",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

GRAMMAR = "phpytex.lark"

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


@dataclass
class Tokeniser:
    _grammar: str | None = field(default=None)
    _lexer: dict[str, Lark] = field(default_factory=dict)

    def parse(self, mode: str, text: str):
        if self._grammar is None:
            self._grammar = get_grammar(GRAMMAR)

        if mode not in self._lexer:
            self._lexer[mode] = Lark(
                self._grammar,
                start=mode,
                regex=True,
                parser="earley",  # 'lalr', 'earley', 'cyk'
                priority="invert",  # auto (default), none, normal, invert
            )

        lexer = self._lexer[mode]

        try:
            return lexer.parse(text)

        except Exception as err:
            err.add_note(f"Could not tokenise input as \033[1m{mode}\033[0m!")
            raise err
