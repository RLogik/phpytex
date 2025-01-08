#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

import logging
import os
import re
from collections import defaultdict
from typing import Any
from typing import Generator

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from ..._core.logging import *
from ..._core.utils.basic import *
from ..._core.utils.misc import *
from ...models.internal import *
from .type_transpileblock import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "TranspileDocument",
    "TranspileDocuments",
]

# ----------------------------------------------------------------
# CLASS transpile document
# ----------------------------------------------------------------


class TranspileDocument(list):
    label: str
    root: str
    path: str
    pathfolder: str
    blocks: TranspileBlocks
    variables: dict[str, Any]
    indentsymb: str

    def __init__(
        self,
        root: str,
        path: str,
        label: str,
        indentsymb: str,
        variables: dict[str, Any] = dict(),
    ):
        self.root = root
        self.pathfolder = os.path.dirname(path) or "."
        self.path = path
        self.label = label
        self.indentsymb = indentsymb
        self.variables = variables
        self.blocks = TranspileBlocks()
        return

    def __len__(self) -> int:
        return len(self.blocks)

    def __iter__(self) -> Generator[TranspileBlock, None, None]:
        for block in self.blocks:
            yield block

    def tab(self, offset: int = 1) -> str:
        return self.indentsymb * offset

    # relativises a path relative to directory to a path relative to root
    def relativisePath(self, path: str):
        if os.path.isabs(path):
            if path.startswith(self.root):
                path = os.path.relpath(path=path, start=self.root)
        else:
            path = os.path.join(self.pathfolder, path)
            path = os.path.relpath(path=path, start=self.root)
        return path

    def append(self, block: TranspileBlock):
        self.blocks.append(block)
        return

    def generateCode(
        self,
        offset: int = 0,
        globalvars: list[str] = [],
        anon: bool = False,
        hide: bool = False,
        align: bool = False,
    ) -> Generator[str, None, None]:
        yield "{tab}# generate content from file '{path}'".format(
            tab=self.tab(offset),
            path=self.path,
        )
        yield "{tab}def {label}():".format(
            tab=self.tab(offset),
            label=self.label,
        )
        yield from TranspileBlock(
            kind="code",
            lines=[
                "global {name};".format(name=name)
                for name in unique(
                    [
                        "__ROOT__",
                        "__DIR__",
                        "__FNAME__",
                        "__ANON__",
                        "__HIDE__",
                        "__IGNORE__",
                        "__MARGIN__",
                        *globalvars,
                    ]
                )
                if name not in ["__STATE__"]
            ]
            + [
                "__ROOT__ = '.';",
                f"__DIR__ = '{self.pathfolder}';" f"__FNAME__ = '{self.path}';",
                "__IGNORE__ = False;",
                f"__ANON__ = {anon};",
                f"__HIDE__ = {hide};",
                "__MARGIN__ = ''",
                "# Save current state locally. Use to restore state after importing subfiles.",
                "__STATE__ = (__ROOT__, __DIR__, __FNAME__, __ANON__, __HIDE__, __IGNORE__);",
            ],
        ).generateCode(offset + 1, anon=False, hide=False, align=align)
        for block in self.blocks:
            yield from block.generateCode(offset + 1, anon=anon, hide=hide, align=align)
        yield "{tab}return;".format(tab=self.tab(offset + 1))
        return


# ----------------------------------------------------------------
# CLASS transpile documents
# ----------------------------------------------------------------


class TranspileDocuments(object):
    root: str
    indentsymb: str
    preamble: dict[str, TranspileBlocks]
    documents: dict[str, TranspileDocument]
    variables: dict[str, Any]
    schemes: dict[str, str]

    paths: list[str]
    anon: defaultdict[str, bool]
    hide: defaultdict[str, bool]
    edges: list[tuple[str, str]]
    docEdges: list[tuple[str, str]]

    def __init__(self, root: str, indentsymb: str, schemes: dict[str, str] = dict()):
        self.root = root
        self.indentsymb = indentsymb
        self.paths = []
        self.documents = dict()
        self.edges = []
        self.docEdges = []
        self.variables = dict()
        self.preamble = dict()
        self.anon = defaultdict(lambda: False)
        self.hide = defaultdict(lambda: False)
        self.schemes = schemes
        return

    def __len__(self) -> int:
        return len(self.documents)

    def tab(self, offset: int = 1) -> str:
        return self.indentsymb * offset

    def updateAnon(self, path: str, initial_value: bool = False):
        """
        Updates anonymity-state, inherit `True`-value from predecessor nodes in document tree.

        @inputs
        - `path` - path to be added as node.
        - `initial_value` - whether or not path is initially forced to be have anon state.

        @returns
        - updated `self.anon`
        """
        self.anon = inheritance_on_graph(self.edges, {path: initial_value, **self.anon})

    def updateHidden(self, path: str, initial_value: bool = False):
        """
        Updates hidden-state, inherit `True`-value from predecessor nodes in document tree.

        @inputs
        - `path` - path to be added as node.
        - `initial_value` - whether or not path is initially forced to be have hidden state.

        @returns
        - updated `self.hide`
        """
        self.hide = inheritance_on_graph(self.edges, {path: initial_value, **self.hide})

    def isAnon(self, path: str) -> bool:
        return self.anon.get(path, False)

    def isHidden(self, path: str) -> bool:
        return self.hide.get(path, False)

    def displayPath(self, path: str) -> str:
        return "#####" if self.anon[path] else path

    def evaluate(self, code_value: str, document: TranspileDocument):
        localvariables = {
            **self.variables,
            **document.variables,
            "__ROOT__": os.path.abspath(document.root),
            "__DIR__": os.path.abspath(document.pathfolder),
        }
        return eval(code_value, None, localvariables)

    def __iter__(self) -> Generator[TranspileDocument, None, None]:
        for _, document in self.documents.items():
            yield document

    def getFunctionName(self, path: str) -> str:
        index = self.paths.index(path)
        return "{label}_{index}".format(label=self.schemes["file"], index=index)

    def get_root_paths(self) -> list[str]:
        has_predecessor = set(v for _, v in self.edges)
        return [path for path in self.paths if path not in has_predecessor]

    def getSubPaths(self, path: str) -> list[str]:
        return [__ for _, __ in self.edges if _ == path]

    def addDocument(self, path: str):
        if path in self.paths:
            return
        self.paths.append(path)
        document = TranspileDocument(
            root=self.root,
            path=os.path.relpath(path=os.path.abspath(path), start=self.root),
            indentsymb=self.indentsymb,
            label=self.getFunctionName(path),
        )
        self.documents[path] = document
        self.updateAnon(path)
        self.updateHidden(path)
        return

    def addPreamble(self, name: str, blocks: TranspileBlocks):
        self.preamble[name] = blocks
        return

    def addBlocks(self, path: str, blocks: TranspileBlocks):
        assert path in self.documents, "Must add document first, before adding blocks."
        document = self.documents[path]
        for block in blocks:
            parameters = block.parameters
            state = dict(level=block.level, indentsymb=block.indentsymb)
            if re.match(r"^text($|:)", block.kind):
                document.append(block)
            elif block.kind == "code":
                document.append(block)
            elif block.kind == "code:escape":
                document.append(block)
            elif block.kind == "code:set":
                var_name = parameters.var_name
                code_value = parameters.code_value
                scope = parameters.scope
                try:
                    value = self.evaluate(code_value, document=document)

                except Exception as _:
                    # TODO: deal with error
                    logging.error(f'Could not evaluate \033[1m<<< {parameters.scope} set {parameters.var_name} = {parameters.code_value} >>>\033[0m.')  # fmt: skip
                    continue
                if scope == "local":
                    document.variables[var_name] = value
                elif scope == "global":
                    self.variables[var_name] = value
                document.append(block)
            elif block.kind == "code:input":
                ## extract block parameters:
                _path = parameters.path
                ## unpack path expression (potentially evaluate):
                try:
                    _path = self.evaluate(parameters.path, document=document)

                except Exception as _:
                    cmd = ('bibliography' if parameters.mode == 'bib' else 'input') \
                        + ('_anon' if parameters.anon else ('_hide' if parameters.hide else ''))  # fmt: skip
                    # TODO: deal with error
                    logging.error(f'Could not evaluate \033[1m<<< {cmd} {parameters.path}\033[0m >>>\033[0m.')  # fmt: skip
                    continue
                _path = document.relativisePath(_path)

                ## add edge for the sake of display (regardless of whether input or bib mode):
                self.docEdges.append((path, _path))
                if parameters.mode == "input":
                    self.edges.append((path, _path))

                self.updateAnon(_path, parameters.anon)
                self.updateHidden(_path, parameters.hide)
                ## create phpytex-code blocks based on computed path:
                if parameters.mode == "input":
                    flabel = self.schemes["file"]
                    document.append(TranspileBlock(kind="text:empty", **state))
                    # force empty line before input of file
                    document.append(
                        TranspileBlock(
                            kind="code",
                            lines=[
                                f"{flabel}('{_path}');",
                                "# Restore state of current file:",
                                "__ROOT__, __DIR__, __FNAME__, __ANON__, __HIDE__, __IGNORE__ = __STATE__;",
                            ],
                            **state,
                        )
                    )
                elif parameters.mode == "bib":
                    document.append(
                        TranspileBlock(
                            kind="code",
                            lines=[
                                f"____insertbib('{_path}', textindent='{parameters.tab}', anon={parameters.anon}, mode='{parameters.bib_mode}', options='{parameters.bib_options}');"
                            ],
                            **state,
                        )
                    )
        document.append(TranspileBlock(kind="text:empty", level=0, indentsymb=self.indentsymb))
        # force empty add end of file
        return

    def as_tree(
        self,
        path: str | None = None,
        /,
    ) -> GenericTree[TranspileDocumentNode]:
        """
        Parses as tree structure
        """
        if path is None:
            root = TranspileDocumentNode()
            paths_children = self.get_root_paths()

        else:
            anon = self.anon[path]
            root = TranspileDocumentNode(path=path, anon=anon)
            paths_children = [v for u, v in self.docEdges if u == path]

        children = [self.as_tree(path) for path in paths_children if not self.hide[path]]

        tree = GenericTree(root=root, children=children)

        return tree

    def __str__(self) -> str:
        tree = self.as_tree()
        return str(tree)

    def documentStamp(self, depth: int, start: bool, anon: bool, hide: bool) -> TranspileBlock:
        return TranspileBlock(
            kind="code",
            content=f"____printfilestamp(depth={depth}, start={start}, anon={anon}, hide={hide});",
            level=0,
            indentsymb=self.indentsymb,
        )

    def documentTree(self, seed: int | None) -> TranspileBlock:
        lines = self.__str__().split("\n")
        return TranspileBlock(
            kind="text:comment",
            lines=dedent_split(
                """
                %% ********************************************************************************
                %% DOCUMENT STRUCTURE:
                %% ~~~~~~~~~~~~~~~~~~~
                %%
                """
            )
            + [f"%% {line}" for line in lines]
            + dedent_split(
                """
                %%
                %% DOCUMENT-RANDOM-SEED: {}
                %% ********************************************************************************
                """.format(seed if isinstance(seed, int) else "---")
            )
            + [""],
            level=0,
            indentsymb=self.indentsymb,
        )

    def generateCode(
        self,
        offset: int = 0,
        preambles: list[str] = [],
        globalvars: list[str] = [],
        anon: bool = False,
        hide: bool = False,
        align: bool = False,
    ) -> Generator[str, None, None]:
        ## generate universal reference function
        yield "{tab}# universal reference function for files".format(tab=self.tab(offset))
        yield "{tab}def {label}(path: str):".format(
            tab=self.tab(offset),
            label=self.schemes["file"],
        )
        for path in self.paths:
            yield "{tab}    if path == '{path}':".format(
                tab=self.tab(offset),
                path=path,
            )
            yield "{tab}        {label}();".format(
                tab=self.tab(offset),
                label=self.getFunctionName(path),
            )
            yield "{tab}        return;".format(tab=self.tab(offset))
        yield "{tab}    raise Exception('{msg}'.format(path));".format(
            msg=r"[\033[91;1mERROR\033[0m] Could not find a method associated to the document path \033[1m{}\033[0m.",
            tab=self.tab(offset),
        )

        ## generate function for preamble parts
        for name, blocks in self.preamble.items():
            yield ""
            yield "{tab}# preamble function '{name}'".format(tab=self.tab(offset), name=name)
            yield "{tab}def {label}():".format(
                tab=self.tab(offset),
                label="{label}_{name}".format(label=self.schemes["pre"], name=name),
            )
            yield from blocks.generateCode(
                offset=offset + 1,
                anon=False,
                hide=False,
                align=align,
            )
            yield "{tab}return".format(tab=self.tab(offset + 1))

        ## generate individual functions for documents
        for path, document in self.documents.items():
            yield ""
            yield from document.generateCode(
                offset=offset,
                globalvars=globalvars,
                anon=self.anon[path],
                hide=self.hide[path],
                align=align,
            )

        ## generate main function, which calls head functions first
        yield ""
        yield "{tab}# generate content from all files".format(tab=self.tab(offset))
        yield "{tab}def {label}():".format(
            tab=self.tab(offset),
            label=self.schemes["main"],
        )
        yield "{tab}____cleardocument();".format(tab=self.tab(offset + 1))
        for name in preambles:
            yield "{tab}{label}();".format(
                tab=self.tab(offset + 1),
                label="{label}_{name}".format(label=self.schemes["pre"], name=name),
            )
        for path in self.get_root_paths():
            yield "{tab}{label}('{path}');".format(
                tab=self.tab(offset + 1),
                label=self.schemes["file"],
                path=path,
            )
        yield "{tab}return;".format(tab=self.tab(offset + 1))
        return


# ----------------------------------------------------------------
# AUXILIARY CLASSES
# ----------------------------------------------------------------


class TranspileDocumentNode(BaseModel):
    """
    Node class for display purposes
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )

    path: str = Field(default=".")
    anon: bool = Field(default=False)

    def __str__(self) -> str:
        return "*****" if self.anon else self.path
