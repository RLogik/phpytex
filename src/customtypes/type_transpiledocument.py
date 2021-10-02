#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.local.misc import *;
from src.local.system import *;
from src.local.typing import *;

from src.core.log import *;
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
    variables: Dict[str, Any];
    indentsymb: str;

    def __init__(
        self,
        root: str,
        path: str,
        fname: str,
        label: str,
        indentsymb: str,
        variables: Dict[str, Any] = dict()
    ):
        self.root = root;
        self.path = path;
        self.fname = fname;
        self.label = label;
        self.indentsymb = indentsymb;
        self.variables = variables;
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

    def addInitialBlock(self):
        self.blocks.insert(0, TranspileBlock(
            kind = 'code',
            lines = [
                "__ROOT__ = '.';".format(),
                "__DIR__ = '{}';".format(self.path),
            ] + [ 'global {var};'.format(key) for key in self.variables.keys() ]
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
        yield '{tab}return;'.format(tab = self.indentsymb * (offset + 1));
        return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile documents
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileDocuments(object):
    root:       str;
    indentsymb: str;
    documents:  Dict[str, TranspileDocument];
    variables:  Dict[str, Any];

    paths:      List[str];
    edges:      List[Tuple[str, str]];

    variables: List[str];

    def __init__(
        self, root: str,
        indentsymb: str,
        variables: Dict[str, Any] = dict()
    ):
        self.root = root;
        self.indentsymb = indentsymb;
        self.paths = [];
        self.documents = dict();
        self.edges = [];
        self.variables = variables;
        return;

    def __len__(self) -> int:
        return len(self.documents);

    def __iter__(self) -> Generator[TranspileDocument, None, None]:
        for _, document in self.documents.items():
            yield document;

    def getFunctionName(self, path: str) -> str:
        index = self.paths.index(path);
        return '{label}_{index}'.format(label=_FUNCTION_NAME_FILE, index=index);

    def getHeadPaths(self) -> List[str]:
        degreeIn = { path: 0 for path in self.paths };
        for u, v in self.edges:
            degreeIn[v] += 1;
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
            label      = self.getFunctionName(path),
            variables  = {
                '__DIR__': os.path.dirname(os.path.abspath(path)),
                '__ROOT__': os.path.abspath('.'),
            }
        );
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
            elif re.match(r'^code:set$', block.kind):
                key = block.parameters['varname'];
                value = block.parameters['value'];
                try:
                    value = eval(value, None, self.variables | document.variables);
                except:
                    ## TODO: deal with error
                    logError('Could not evaluate <<< set \033[1m{}\033[0m >>>.'.format(value));
                    continue;
                if re.match(r':local$', block.kind):
                    self.variables[key] = value;
                elif re.match(r':global$', block.kind):
                    document.variables[key] = value;
                document.append(block);
            elif re.match(r'^code:input', block.kind):
                _path = block.parameters['path'];
                try:
                    _path = eval(_path, None, self.variables | document.variables);
                except:
                    logError('Could not evaluate <<< input \033[1m{}\033[0m >>>.'.format(_path));
                    continue;
                _path = os.path.relpath(_path, self.root);
                self.edges.append((path, _path));
                document.append(TranspileBlock(
                    kind        = 'code',
                    content     = '{label}(\'{path}\');'.format(
                        label = _FUNCTION_NAME_FILE,
                        path  = _path,
                    ),
                    indentlevel = block.indentlevel,
                    indentsymb  = block.indentsymb
                ));
            elif re.match(r'^code:bib', block.kind):
                # TODO
                pass;
        return;

    def generateCode(self, offset: int = 0) -> Generator[str, None, None]:
        ## generate universal reference function
        yield '';
        yield '{tab}# universal reference function for files'.format(tab = self.indentsymb * offset);
        yield '{tab}def {label}(path: str):'.format(
            tab   = self.indentsymb * offset,
            label = _FUNCTION_NAME_FILE,
        );
        for path in self.paths:
            yield '{tab}    if path == \'{path}\':'.format(
                tab  = self.indentsymb * offset,
                path = path,
            );
            yield '{tab}        {label}();'.format(
                tab = self.indentsymb * offset,
                path = path,
                label = self.getFunctionName(path),
            )
        yield '{tab}    raise Exception(\'{msg}\'.format(path));'.format(
            msg = '[\033[91;1mERROR\033[0m] Could not find a method associated to the document path \033[1m{}\033[0m.',
            tab = self.indentsymb * offset,
        );

        ## generate universal individual functions for documents
        for document in self.documents.values():
            yield '';
            yield from document.generateCode(offset=offset);

        ## generate main function, which calls head functions first
        yield '';
        yield '{tab}# generate content from all files'.format(tab = self.indentsymb * offset);
        yield '{tab}def {label}():'.format(
            tab   = self.indentsymb * offset,
            label = _FUNCTION_NAME_MAIN,
        );
        for path in self.getHeadPaths():
            yield '{tab}{label}();'.format(
                tab  = self.indentsymb * (offset + 1),
                label = self.getFunctionName(path),
            );
        yield '{tab}return;'.format(tab = self.indentsymb * (offset + 1));
        return;
