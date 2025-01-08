#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from lark import Lark
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

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


class TokeniserStruct(BaseModel):
    """
    Underlying struct for tokeniser.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    grammar: str | None = Field(default=None)
    lexer: dict[str, Lark] = Field(default_factory=dict)


class Tokeniser(TokeniserStruct):
    """
    A class wrapper for lexing/parsing grammars.
    """

    def parse(
        self,
        text: str,
        /,
        *,
        mode: str,
    ):
        if self.grammar is None:
            # TODO: this should not be done here. -> refactor code!
            from ...setup import get_grammar

            self.grammar = get_grammar(GRAMMAR)

        lexer = self.lexer.get(mode)
        if lexer is None:
            lexer = Lark(
                self.grammar,
                start=mode,
                regex=True,
                parser="earley",  # 'lalr', 'earley', 'cyk'
                priority="invert",  # auto (default), none, normal, invert
            )
            self.lexer[mode] = lexer

        try:
            return lexer.parse(text)

        except Exception as err:
            err.add_note(f"Could not tokenise input as \033[1m{mode}\033[0m!")
            raise err
