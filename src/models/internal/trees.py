#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

from typing import Generator
from typing import Generic
from typing import Literal
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "GenericTree",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS, VARIABLES
# ----------------------------------------------------------------

T = TypeVar("T")
R = TypeVar("R")

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class GenericTree(BaseModel, Generic[T]):
    """
    A generic for handling trees
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    root: T
    children: list[T | GenericTree[T]] = Field(default_factory=list)

    def __str__(self) -> str:
        lines = list(self._recursive_repr(self.root))
        return "\n".join(lines)

    def add(self, other: T | GenericTree[T]):
        self.children.append(other)

    @staticmethod
    def _repr_node(
        node: T,
        /,
        *,
        indent: str = "  ",
        lex: list[bool] = [],
        sep: str = "",
    ) -> str:
        """
        Displays a single node
        """
        prefix = "".join([
            (" " if is_last else "│") + indent
            for is_last in lex[:-1]
        ])  # fmt: skip
        return f"{prefix}{sep}{node}"

    def _recursive_repr(
        self,
        node: T | None = None,
        /,
        *,
        indent: str = "  ",
        lex: list[bool] = [],
        sep: str = "",
    ) -> Generator[str, None, None]:
        """
        Method to recursive display elements of Tree
        """
        if node is None:
            node = self.root

        yield GenericTree._repr_node(node, indent=indent, lex=lex, sep=sep)

        n = len(self.children)
        for k, child in enumerate(self.children):
            is_final = k == n - 1
            if isinstance(child, GenericTree):
                yield from child._recursive_repr(
                    child.root,
                    indent=indent,
                    lex=[*lex, is_final],
                    sep="└──  " if is_final else "├──  ",
                )

            else:
                yield GenericTree._repr_node(
                    child,
                    indent=indent,
                    lex=[*lex, is_final],
                    sep="└──  " if is_final else "├──  ",
                )

        return

    def walk(
        self,
        *,
        mode: Literal["ROOT-FIRST", "CHILDREN-FIRST"] = "ROOT-FIRST",
        include_root: bool = True,
    ) -> Generator[T, None, None]:
        """
        Traverses the tree
        """
        if mode == "ROOT-FIRST" and include_root:
            yield self.root

        for child in self.children:
            if isinstance(child, GenericTree):
                yield from child.walk(mode=mode, include_root=True)

            else:
                yield child
        if mode == "CHILDREN-FIRST" and include_root:
            yield self.root

        return
