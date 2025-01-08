#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

import re
from typing import Any
from typing import Generator

from ..._core.utils.basic import *
from ..._core.utils.misc import *
from ...models.generated.app import *
from ...parsers import parser_python

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "TranspileBlock",
    "TranspileBlocks",
]

# ----------------------------------------------------------------
# CLASS transpile block
# ----------------------------------------------------------------


class TranspileBlock(object):
    kind: str
    _content: str
    lines: list[str]
    level: int
    indentsymb: str
    parameters: TranspileBlockParameters
    margin: str
    subst: dict[str, TranspileBlock]

    def __init__(
        self,
        kind: str,
        content: Any = None,
        lines: list[str] = [],
        level: int = 0,
        indentsymb: str = "    ",
        parameters: TranspileBlockParameters = TranspileBlockParameters(),
        margin: str = "",
        **_,
    ):
        self.lines = lines
        self.kind = kind
        self.level = level
        self.indentsymb = indentsymb
        self.parameters = TranspileBlockParameters.model_validate(parameters)
        self.margin = margin
        self.subst = dict()
        if isinstance(content, str):
            self._content = content
        return

    @property
    def isCode(self) -> bool:
        return True if re.match(r"^code(:|$)", self.kind) else False

    @property
    def content(self) -> Generator[str, None, None]:
        tab = self.tab() if self.isCode else ""
        if hasattr(self, "_content"):
            yield "{tab}{line}".format(tab=tab, line=self._content)
        else:
            yield from reindent_lines(self.lines, indent=tab, unindent=False)

    def tab(self, delta: int = 0) -> str:
        return self.indentsymb * (self.level + delta)

    def generateCode(
        self,
        offset: int = 0,
        anon: bool = False,
        hide: bool = False,
        align: bool = False,
    ) -> Generator[str, None, None]:
        state = dict(level=self.level, indentsymb=self.indentsymb)
        self.level += offset
        if self.kind == "text:empty":
            yield "{tab}____print('', anon={anon}, hide={hide}, align={align});".format(
                tab=self.tab(),
                anon=anon,
                hide=hide,
                align=align,
            )
        elif self.kind in ["text", "text:comment"]:
            for line in self.content:
                yield "{tab}____print('''{expr}''', anon={anon}, hide={hide}, align={align});".format(
                    tab=self.tab(),
                    expr=parser_python.escape_code(line, fmt=False),
                    anon=anon,
                    hide=hide,
                    align=align,
                )
        elif self.kind == "text:subst":
            if len(self.subst) == 0:
                yield "{tab}____print('''{expr}'''.format(), anon={anon}, hide={hide}, align={align});".format(
                    tab=self.tab(),
                    expr="\n".join(list(self.content)),
                    anon=anon,
                    hide=hide,
                    align=align,
                )
            else:
                yield "{tab}__MARGIN__ = '{margin}';".format(
                    tab=self.tab(),
                    margin=self.margin,
                )
                yield "{tab}____print('''{expr}'''.format(".format(
                    tab=self.tab(),
                    expr="\n".join(list(self.content)),
                )
                for key, value in self.subst.items():
                    level = value.level
                    value_lines = reindent_lines(
                        value.lines,
                        indent=self.tab(2),
                        unindent=True,
                    )
                    value_lines[0] = re.sub(r"^\s*(.*)$", r"\1", value_lines[0])
                    yield "{tab}{key} = {value},".format(
                        tab=self.tab(1),
                        key=key,
                        value="\n".join(value_lines),
                    )
                    value.level = level
                yield "{tab}), anon={anon}, hide={hide}, align={align});".format(
                    tab=self.tab(),
                    anon=anon,
                    hide=hide,
                    align=align,
                )
        elif self.kind in ["code", "code:import", "code:value"]:
            yield from self.content
        elif self.kind == "code:set":
            line = f"{self.parameters.var_name} = {self.parameters.code_value};"
            block = TranspileBlock(kind="code", content=line, **state)
            yield from block.generateCode(offset=offset, align=align)
        elif self.kind == "code:escape":
            block = TranspileBlock(kind="code", content="pass;", **state)
            yield from block.generateCode(offset=offset, align=align)
        elif self.kind == "code:input":
            pass
        self.level = state["level"]
        return


class TranspileBlocks(object):
    blocks: list[TranspileBlock]

    def __init__(self, blocks: list[TranspileBlock] = []):
        self.blocks = blocks[:]

    def __len__(self) -> int:
        return len(self.blocks)

    def __iter__(self) -> Generator[TranspileBlock, None, None]:
        for block in self.blocks:
            yield block
        return

    def append(self, block: TranspileBlock):
        self.blocks.append(block)

    def generateCode(
        self,
        offset: int = 0,
        anon: bool = False,
        hide: bool = False,
        align: bool = False,
    ) -> Generator[str, None, None]:
        for block in self.blocks:
            yield from block.generateCode(offset=offset, anon=anon, hide=hide, align=align)
        return
