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
    def is_code(self) -> bool:
        return True if re.match(r"^code(:|$)", self.kind) else False

    @property
    def content(self) -> Generator[str, None, None]:
        tab = self.tab() if self.is_code else ""

        if hasattr(self, "_content"):
            yield "{tab}{line}".format(tab=tab, line=self._content)

        else:
            yield from reindent_lines(*self.lines, indent=tab, unindent=False)

    def tab(self, delta: int = 0) -> str:
        return self.indentsymb * (self.level + delta)

    def generate_code(
        self,
        offset: int = 0,
        anon: bool = False,
        hide: bool = False,
        align: bool = False,
    ) -> Generator[str, None, None]:
        state = dict(level=self.level, indentsymb=self.indentsymb)
        self.level += offset

        match self.kind, self.subst:
            case "text:empty", _:
                yield "{tab}____print('', anon={anon}, hide={hide}, align={align})".format(
                    tab=self.tab(),
                    anon=anon,
                    hide=hide,
                    align=align,
                )

            case "text" | "text:comment", _:
                for line in self.content:
                    yield "{tab}____print('''{expr}''', anon={anon}, hide={hide}, align={align})".format(
                        tab=self.tab(),
                        expr=parser_python.escape_code(line, fmt=False),
                        anon=anon,
                        hide=hide,
                        align=align,
                    )

            case "text:subst", subst if len(subst) == 0:
                yield "{tab}____print('''{expr}'''.format(), anon={anon}, hide={hide}, align={align})".format(
                    tab=self.tab(),
                    expr="\n".join(list(self.content)),
                    anon=anon,
                    hide=hide,
                    align=align,
                )

            case "text:subst", _:
                yield "{tab}__MARGIN__ = '{margin}'".format(
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
                        *value.lines,
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
                yield "{tab}), anon={anon}, hide={hide}, align={align})".format(
                    tab=self.tab(),
                    anon=anon,
                    hide=hide,
                    align=align,
                )

            case "code" | "code:import" | "code:value", _:
                yield from self.content

            case "code:set", _:
                line = f"{self.parameters.var_name} = {self.parameters.code_value}"
                block = TranspileBlock(kind="code", content=line, **state)
                yield from block.generate_code(offset=offset, align=align)

            case "code:escape", _:
                block = TranspileBlock(kind="code", content="pass", **state)
                yield from block.generate_code(offset=offset, align=align)

            case "code:input", _:
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

    def generate_code(
        self,
        offset: int = 0,
        anon: bool = False,
        hide: bool = False,
        align: bool = False,
    ) -> Generator[str, None, None]:
        for block in self.blocks:
            yield from block.generate_code(offset=offset, anon=anon, hide=hide, align=align)
        return
