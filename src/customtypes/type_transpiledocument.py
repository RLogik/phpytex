#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations

from src.local.misc import *;
from src.local.system import *;
from src.local.typing import *;

from src.customtypes.type_transpileblock import TranspileBlock;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_FUNCTION_NAME_FILE: str = '_phpytex_generate_file';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile document
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileDocument(list):
    label: str;
    root: str;
    path: str;
    blocks: List[TranspileBlock];
    indentsymb: str;

    def __init__(
        self,
        root: str,
        path: str,
        label: str,
        indentsymb: str
    ):
        self.root = root;
        self.path = path;
        self.label = label;
        self.indentsymb = indentsymb;
        self.blocks = [];
        return;

    @property
    def pathRelativeToRoot(self) -> str:
        return os.path.dirname(os.path.relpath(self.path, self.root));

    @property
    def rootRelativeToPath(self) -> str:
        return os.path.relpath(self.root, os.path.dirname(self.path));

    def addBlock(self, block: TranspileBlock):
        self.blocks.append(block);
        return;

    def generateCode(self, offset: int = 0) -> Generator[str, None, None]:
        yield '{tab}# generate content from file `{path}`'.format(
            tab  = self.indentsymb * offset,
            path = self.path
        );
        yield '{tab}def {label}():'.format(
            tab  = self.indentsymb * offset,
            label = self.label,
        );
        for block in self.blocks:
            yield from block.generateCode(offset + 1);
        return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile documents
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileDocuments(object):
    root:       str;
    indentsymb: str;
    documents:  Dict[str, TranspileDocument];
    paths:      List[str];
    edges:      List[Tuple[str, str]];

    def __init__(self, root: str, indentsymb: str):
        self.root = root;
        self.indentsymb = indentsymb;
        self.paths = [];
        self.documents = dict();
        self.edges = [];
        return;

    def __len__(self) -> int:
        return len(self.paths);

    def addDocument(self, path: str):
        if path in self.paths:
            return;
        self.paths.append(path);
        index = self.paths.index(path);
        document = TranspileDocument(
            root       = self.root,
            path       = path,
            indentsymb = self.indentsymb,
            label      = '{fname}_{index}'.format(fname=_FUNCTION_NAME_FILE, index=index)
        );
        self.documents[path] = document;
        return;

    def addBlocks(self, path: str, blocks: List[TranspileBlock]):
        assert path in self.documents, 'Must add document first, before adding blocks.';
        document = self.documents[path];
        document.addBlock(TranspileBlock(
            kind = 'code',
            lines = [
                "__ROOT__ = '{}';".format(document.rootRelativeToPath),
                "__DIR__ = '{}';".format(document.pathRelativeToRoot),
            ]
        ))
        for block in blocks:
            if re.match(r'^text($|:)', block.kind):
                document.append(block);
            elif re.match(r'^code:(set|escape)', block.kind):
                document.append(block);
            elif re.match(r'^code:input', block.kind):
                _path = block.parameters['path'];
                self.addDocument(_path);
                self.edges.append((path, _path));
                _index = self.paths.index(_path);
                document.append(TranspileBlock(
                    kind        = 'code',
                    content     = '{fname}_{index}'.format(fname=_FUNCTION_NAME_FILE, index=_index),
                    indentlevel = block.indentlevel,
                    indentsymb  = block.indentsymb
                ));
            elif re.match(r'^code:bib', block.kind):
                # TODO
                pass;
        self.documents[path] = document;
        return;

    def generateCode(self, offset: int = 0) -> Generator[str, None, None]:
        for document in self.documents.values():
            yield '';
            yield from document.generateCode(offset=offset);
        return;
