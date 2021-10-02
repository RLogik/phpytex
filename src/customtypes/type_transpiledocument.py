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

_FUNCTION_NAME_MAIN: str = '_phpytex_generate_main';
_FUNCTION_NAME_FILE: str = '_phpytex_generate_file';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile document
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileDocument(list):
    label: str;
    root: str;
    path: str;
    fname: str;
    blocks: List[TranspileBlock];
    indentsymb: str;

    def __init__(
        self,
        root: str,
        path: str,
        fname: str,
        label: str,
        indentsymb: str
    ):
        self.root = root;
        self.path = path;
        self.fname = fname;
        self.label = label;
        self.indentsymb = indentsymb;
        self.blocks = [];
        return;

    def __len__(self) -> int:
        return len(self.blocks);

    def __iter__(self) -> Generator[TranspileBlock, None, None]:
        for block in self.blocks:
            yield block;

    def pathRelativeToRoot(self, path: str) -> str:
        return os.path.relpath(path, self.root);

    def rootRelativeToDocumentDir(self, path: str) -> str:
        return os.path.relpath(path, self.path);

    def append(self, block: TranspileBlock):
        self.blocks.append(block);
        return;

    def addInitialBlock(self, globalvars: Dict[str, Any]):
        self.blocks.insert(0, TranspileBlock(
            kind = 'code',
            lines = [
                "__ROOT__ = '.';".format(),
                "__DIR__ = '{}';".format(self.path),
            ] + [ 'global {var};'.format(key) for key in globalvars.keys() ]
        ));
        return;

    def generateCode(self, offset: int = 0) -> Generator[str, None, None]:
        yield '{tab}# generate content from file `{path}`'.format(
            tab  = self.indentsymb * offset,
            path = os.path.join(self.path, self.fname),
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
    degreeIn:   Dict[str, int];
    degreeOut:  Dict[str, int];

    globalvars: List[str];

    def __init__(self, root: str, indentsymb: str):
        self.root = root;
        self.indentsymb = indentsymb;
        self.paths = [];
        self.documents = dict();
        self.edges = [];
        self.degreeIn = dict();
        self.degreeOut = dict();
        self.globalvars = [];
        return;

    def __len__(self) -> int:
        return len(self.documents);

    def __iter__(self) -> Generator[TranspileDocument, None, None]:
        for _, document in self.documents.items():
            yield document;

    def getFunctionName(self, path: str) -> str:
        index = self.paths.index(path);
        return '{fname}_{index}'.format(fname=_FUNCTION_NAME_FILE, index=index);

    def getHeadPaths(self) -> List[str]:
        return [ path for path in self.paths if self.degreeIn[path] == 0 ];

    def getSubPaths(self, path: str) -> List[str]:
        return [ __ for _, __ in self.edges if _ == path ];

    def addDocument(self, path: str):
        if path in self.paths:
            return;
        self.paths.append(path);
        document = TranspileDocument(
            root       = self.root,
            path       = os.path.dirname(path),
            fname      = os.path.basename(path),
            indentsymb = self.indentsymb,
            label      = self.getFunctionName(path)
        );
        self.degreeIn[path] = 0;
        self.degreeOut[path] = 0;
        self.documents[path] = document;
        return;

    def addBlocks(self, path: str, blocks: List[TranspileBlock]):
        assert path in self.documents, 'Must add document first, before adding blocks.';
        document = self.documents[path];
        for block in blocks:
            if re.match(r'^text($|:)', block.kind):
                document.append(block);
            elif re.match(r'^code($|:escape)', block.kind):
                document.append(block);
            elif re.match(r'^code:set', block.kind):
                self.globalvars.append(block.parameters['varname']);
                document.append(block);
            elif re.match(r'^code:input', block.kind):
                _path = block.parameters['path'];
                self.addDocument(_path);
                self.edges.append((path, _path));
                self.degreeOut[path] += 1;
                self.degreeIn[_path] += 1;
                document.append(TranspileBlock(
                    kind        = 'code',
                    content     = '{label}();'.format(
                        label = self.getFunctionName(_path),
                    ),
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
        yield '';
        yield '{tab}# generate content from all files'.format(
            tab  = self.indentsymb * offset,
        );
        yield '{tab}def {label}():'.format(
            tab  = self.indentsymb * offset,
            label = _FUNCTION_NAME_MAIN,
        );
        for path in self.getHeadPaths():
            yield '{tab}{label}();'.format(
                tab  = self.indentsymb * (offset + 1),
                label = self.getFunctionName(path),
            );
        return;
