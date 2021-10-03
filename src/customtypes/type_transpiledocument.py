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
from src.core.utils import formatTextBlockAsList;
from src.parsers.methods import escapeForPython;
from src.customtypes.type_transpileblock import TranspileBlock;
from src.customtypes.type_transpileblock import TranspileBlocks;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_FUNCTION_NAME_MAIN: str = '_phpytex_generate_main';
_FUNCTION_NAME_FILE: str = '_phpytex_generate_file';
_FUNCTION_NAME_PRE:  str = '_phpytex_generate_pre';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile document
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileDocument(list):
    label: str;
    root: str;
    path: str;
    pathfolder: str;
    blocks: TranspileBlocks;
    variables: Dict[str, Any];
    indentsymb: str;

    def __init__(
        self,
        root: str,
        path: str,
        label: str,
        indentsymb: str,
        variables: Dict[str, Any] = dict()
    ):
        self.root = root;
        self.pathfolder = os.path.dirname(path) or '.';
        self.path = path;
        self.label = label;
        self.indentsymb = indentsymb;
        self.variables = variables;
        self.blocks = TranspileBlocks();
        return;

    def __len__(self) -> int:
        return len(self.blocks);

    def __iter__(self) -> Generator[TranspileBlock, None, None]:
        for block in self.blocks:
            yield block;

    # relativises a path relative to directory to a path relative to root
    def relativisePath(self, path: str):
        if not os.path.isabs(path):
            path = os.path.join(self.pathfolder, path);
            path = os.path.relpath(path=path, start=self.root);
        return path;

    def append(self, block: TranspileBlock):
        self.blocks.append(block);
        return;

    def generateCode(
        self,
        offset:     int       = 0,
        globalvars: List[str] = []
    ) -> Generator[str, None, None]:
        yield '{tab}# generate content from file `{path}`'.format(
            tab  = self.indentsymb * offset,
            path = self.path,
        );
        yield '{tab}def {label}():'.format(
            tab  = self.indentsymb * offset,
            label = self.label,
        );
        yield from TranspileBlock(
            kind = 'code',
            lines = [
                'global {name};'.format(name=name)
                for name in globalvars if not name in [ '__ROOT__', '__DIR__']
            ] + [
                '__ROOT__ = \'.\';'.format(),
                '__DIR__ = \'{path}\';'.format(path = self.pathfolder),
            ]
        ).generateCode(offset + 1);
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
    preamble:   Dict[str, TranspileBlocks];
    documents:  Dict[str, TranspileDocument];
    parameters: Dict[str, Any];
    variables:  Dict[str, Any];

    paths:      List[str];
    anon:       Dict[str, bool];
    edges:      List[Tuple[str, str]];

    variables: List[str];

    def __init__(
        self, root: str,
        indentsymb: str,
        parameters: Dict[str, Any] = dict(),
        variables: Dict[str, Any] = dict()
    ):
        self.root = root;
        self.indentsymb = indentsymb;
        self.paths = [];
        self.documents = dict();
        self.edges = [];
        self.parameters = parameters;
        self.variables = variables;
        self.preamble = dict();
        self.anon = dict();
        return;

    def __len__(self) -> int:
        return len(self.documents);

    def evaluate(self, codevalue: str, document: TranspileDocument):
        localvariables = self.variables | document.variables | {
            '__ROOT__': os.path.abspath(document.root),
            '__DIR__': os.path.abspath(document.pathfolder),
        };
        return eval(codevalue, None, localvariables);

    def __iter__(self) -> Generator[TranspileDocument, None, None]:
        for _, document in self.documents.items():
            yield document;

    def getFunctionName(self, path: str) -> str:
        index = self.paths.index(path);
        return '{label}_{index}'.format(label=_FUNCTION_NAME_FILE, index=index);

    def getHeadPaths(self) -> List[str]:
        degreeIn = { path: 0 for path in self.paths };
        for u, v in self.edges:
            degreeIn[v] = degreeIn[v] + 1 if v in degreeIn else 0;
        return [ path for path in self.paths if degreeIn[path] == 0 ];

    def getSubPaths(self, path: str) -> List[str]:
        return [ __ for _, __ in self.edges if _ == path ];

    def addDocument(self, path: str):
        if path in self.paths:
            return;
        self.paths.append(path);
        document = TranspileDocument(
            root       = self.root,
            path       = os.path.relpath(path=os.path.abspath(path), start=self.root),
            indentsymb = self.indentsymb,
            label      = self.getFunctionName(path)
        );
        self.documents[path] = document;
        self.anon[path] = self.anon[path] if path in self.anon else False;
        return;

    def addPreamble(self, name: str, blocks: TranspileBlocks):
        self.preamble[name] = blocks;
        return;

    def addBlocks(self, path: str, blocks: TranspileBlocks):
        assert path in self.documents, 'Must add document first, before adding blocks.';
        document = self.documents[path];
        for block in blocks:
            if re.match(r'^text($|:)', block.kind):
                document.append(block);
            elif re.match(r'^code($|:escape)', block.kind):
                document.append(block);
            elif re.match(r'^code:set', block.kind):
                key = block.parameters['varname'];
                codevalue = block.parameters['codevalue'];
                try:
                    value = self.evaluate(codevalue, document=document);
                except:
                    ## TODO: deal with error
                    logError('Could not evaluate <<< set \033[1m{}\033[0m >>>.'.format(value));
                    continue;
                if re.match(r'^.*:local$', block.kind):
                    document.variables[key] = value;
                elif re.match(r'^.*:global$', block.kind):
                    self.variables[key] = value;
                document.append(block);
            elif re.match(r'^code:input', block.kind):
                _path = block.parameters['path'];
                try:
                    _path = self.evaluate(_path, document=document);
                except:
                    logError('Could not evaluate <<< input \033[1m{}\033[0m >>>.'.format(_path));
                    continue;
                _path = document.relativisePath(_path);
                self.edges.append((path, _path));
                self.anon[_path] = True if re.match(r'^.*:anon$', block.kind) else False;
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

    def documentStructurePretty(
        self,
        path = None,
        prefix: str = '',
        indentsymb: str = '    ',
        branchsymb: str = '  |____',
        depth: int = 0
    ) -> Generator[str, None, None]:
        if not isinstance(path, str):
            depth = 0;
            children = self.getHeadPaths();
        elif path in self.paths:
            yield '{prefix}{tab}{branchsymb}`{path}`'.format(
                prefix = prefix,
                tab = indentsymb*(depth if depth == 0 else depth - 1),
                branchsymb = '' if depth == 0 else branchsymb,
                path = '#####' if self.anon[path] else path,
            );
            depth = depth + 1;
            children = [ v for u, v in self.edges if u == path ];
        else:
            return;
        for subpath in children:
            yield from self.documentStructurePretty(subpath, prefix=prefix, indentsymb=indentsymb, branchsymb=branchsymb, depth=depth);
        return;

    def documentTree(self, seed: int) -> TranspileBlock:
        return TranspileBlock(
            kind = 'text:comment',
            lines = formatTextBlockAsList(
                    '''
                    %% ********************************************************************************
                    %% DOCUMENT STRUCTURE:
                    %% ~~~~~~~~~~~~~~~~~~~
                    %%
                    '''
                ) \
                + list(self.documentStructurePretty(prefix='%% ')) \
                + formatTextBlockAsList(
                    '''
                    %%
                    %% DOCUMENT-RANDOM-SEED: {}'
                    %% ********************************************************************************
                    '''.format(seed)
                ),
            indentlevel = 0,
            indentsymb = self.indentsymb,
        );

    def generateCode(
        self,
        offset:     int       = 0,
        preamble:   List[str] = [],
        globalvars: List[str] = []
    ) -> Generator[str, None, None]:
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

        ## generate function for preamble parts
        for name, blocks in self.preamble.items():
            yield '';
            yield '{tab}# '.format(tab = self.indentsymb * offset)
            yield '{tab}def {label}():'.format(
                tab   = self.indentsymb * offset,
                label = '{label}_{name}'.format(label=_FUNCTION_NAME_PRE, name=name),
            );
            yield from blocks.generateCode(offset=offset+1);
            yield '{tab}return'.format(tab = self.indentsymb * (offset + 1));

        ## generate individual functions for documents
        for document in self.documents.values():
            yield '';
            yield from document.generateCode(offset=offset, globalvars=globalvars);

        ## generate main function, which calls head functions first
        yield '';
        yield '{tab}# generate content from all files'.format(tab = self.indentsymb * offset);
        yield '{tab}def {label}():'.format(
            tab   = self.indentsymb * offset,
            label = _FUNCTION_NAME_MAIN,
        );
        for name in preamble:
            yield '{tab}{label}();'.format(
                tab  = self.indentsymb * (offset + 1),
                label = '{label}_{name}'.format(label=_FUNCTION_NAME_PRE, name=name),
            );
        for path in self.getHeadPaths():
            yield '{tab}# {path}'.format(
                tab  = self.indentsymb * (offset + 1),
                path = path,
            );
            yield '{tab}{label}();'.format(
                tab  = self.indentsymb * (offset + 1),
                label = self.getFunctionName(path),
            );
        yield '{tab}return;'.format(tab = self.indentsymb * (offset + 1));
        return;
