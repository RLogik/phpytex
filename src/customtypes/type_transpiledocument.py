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
from src.core.utils import getAttribute;
from src.core.utils import unique;
from src.customtypes.type_transpileblock import TranspileBlock;
from src.customtypes.type_transpileblock import TranspileBlocks;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

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

    def tab(self, offset: int = 1) -> str:
        return self.indentsymb * offset;

    # relativises a path relative to directory to a path relative to root
    def relativisePath(self, path: str):
        if os.path.isabs(path):
            if path.startswith(self.root):
                path = os.path.relpath(path=path, start=self.root);
        else:
            path = os.path.join(self.pathfolder, path);
            path = os.path.relpath(path=path, start=self.root);
        return path;

    def append(self, block: TranspileBlock):
        self.blocks.append(block);
        return;

    def generateCode(
        self,
        offset:     int       = 0,
        globalvars: List[str] = [],
        anon:       bool      = False
    ) -> Generator[str, None, None]:
        yield '{tab}# generate content from file \'{path}\''.format(
            tab  = self.tab(offset),
            path = self.path,
        );
        yield '{tab}def {label}():'.format(
            tab  = self.tab(offset),
            label = self.label,
        );
        yield from TranspileBlock(
            kind = 'code',
            lines = [
                'global {name};'.format(name=name)
                for name in unique([ '__ROOT__', '__DIR__', '__FNAME__', '__ANON__', '__IGNORE__' ] + globalvars)
                if not name in [ '__STATE__' ]
            ] + [
                '__ROOT__ = \'.\';'.format(),
                '__DIR__ = \'{path}\';'.format(path = self.pathfolder),
                '__FNAME__ = \'{path}\';'.format(path = self.path),
                '__IGNORE__ = False;',
                '__ANON__ = {};'.format(anon),
                '# Save current state locally. Use to restore state after importing subfiles.',
                '__STATE__ = (__ROOT__, __DIR__, __FNAME__, __ANON__, __IGNORE__);',
            ]
        ).generateCode(offset + 1);
        for block in self.blocks:
            yield from block.generateCode(offset + 1);
        yield '{tab}return;'.format(tab=self.tab(offset + 1));
        return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile documents
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileDocuments(object):
    root:       str;
    indentsymb: str;
    preamble:   Dict[str, TranspileBlocks];
    documents:  Dict[str, TranspileDocument];
    variables:  Dict[str, Any];
    schemes:    Dict[str, str];

    paths:      List[str];
    anon:       Dict[str, bool];
    edges:      List[Tuple[str, str]];
    docEdges:   List[Tuple[str, str]];

    variables:  List[str];

    def __init__(
        self,
        root: str,
        indentsymb: str,
        schemes:    Dict[str, str] = dict()
    ):
        self.root = root;
        self.indentsymb = indentsymb;
        self.paths = [];
        self.documents = dict();
        self.edges = [];
        self.docEdges = [];
        self.variables = dict();
        self.preamble = dict();
        self.anon = dict();
        self.schemes = schemes;
        return;

    def __len__(self) -> int:
        return len(self.documents);

    def tab(self, offset: int = 1) -> str:
        return self.indentsymb * offset;

    def isAnon(self, path: str) -> bool:
        if (path in self.anon) and self.anon[path]:
            return True;
        for u, v in self.edges:
            if v == path and (u in self.anon) and self.anon[u]:
                return True;
        return False;

    def displayPath(self, path: str) -> str:
        return '#####' if self.isAnon(path) else path;

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
        return '{label}_{index}'.format(label=self.schemes['file'], index=index);

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
        self.anon[path] = self.isAnon(path);
        return;

    def addPreamble(self, name: str, blocks: TranspileBlocks):
        self.preamble[name] = blocks;
        return;

    def addBlocks(self, path: str, blocks: TranspileBlocks):
        assert path in self.documents, 'Must add document first, before adding blocks.';
        document = self.documents[path];
        for block in blocks:
            state = dict(level=block.level, indentsymb=block.indentsymb);
            if re.match(r'^text($|:)', block.kind):
                document.append(block);
            elif block.kind == 'code':
                document.append(block);
            elif block.kind == 'code:escape':
                document.append(block);
            elif block.kind == 'code:set':
                varname   = block.parameters.varname;
                codevalue = block.parameters.codevalue;
                scope     = block.parameters.scope;
                try:
                    value = self.evaluate(codevalue, document=document);
                except:
                    ## TODO: deal with error
                    logError('Could not evaluate \033[1m<<< {scope} set {varname} = {codevalue} >>>\033[0m.'.format(
                        scope   = scope,
                        varname = varname,
                        codevalue = codevalue,
                    ));
                    continue;
                if scope == 'local':
                    document.variables[varname] = value;
                elif scope == 'global':
                    self.variables[varname] = value;
                document.append(block);
            elif block.kind == 'code:input':
                ## extract block parameters:
                _path      = block.parameters.path;
                anon       = block.parameters.anon;
                mode       = block.parameters.mode;
                textindent = block.parameters.tab;
                ## unpack path expression (potentially evaluate):
                try:
                    _path = self.evaluate(_path, document=document);
                except:
                    ## TODO: deal with error
                    logError('Could not evaluate \033[1m<<< {cmd} {path}\033[0m >>>\033[0m.'.format(
                        cmd  = ('bibliography' if mode == 'bib' else 'input') + ('_anon' if anon else ''),
                        path = _path,
                    ));
                    continue;
                _path = document.relativisePath(_path);
                ## add edge for the sake of display (regardless of whether input or bib mode):
                self.docEdges.append((path, _path));
                if not (_path in self.anon):
                    self.anon[_path] = False;
                self.anon[_path] = anon or self.anon[_path];
                ## create phpytex-code blocks based on computed path:
                if mode == 'input':
                    self.edges.append((path, _path));
                    document.append(TranspileBlock(kind='text:empty', **state)); # force empty line before input of file
                    document.append(TranspileBlock(
                        kind        = 'code',
                        lines       = [
                            '{label}(\'{path}\');'.format(label=self.schemes['file'], path=_path),
                            '# Restore state of current file:',
                            '__ROOT__, __DIR__, __FNAME__, __ANON__, __IGNORE__ = __STATE__;',
                        ],
                        **state
                    ));
                elif mode == 'bib':
                    document.append(TranspileBlock(
                        kind           = 'code',
                        lines          = [
                            '____insertbib(\'{fname}\', textindent=\'{textindent}\', anon={anon});'.format(
                                fname      = _path,
                                textindent = textindent,
                                anon       = anon,
                            )
                        ],
                        **state
                    ));
        document.append(TranspileBlock(kind='text:empty', level=0, indentsymb=self.indentsymb)); # force empty add end of file
        return;

    def documentStructurePretty(
        self,
        path = None,
        anon:       bool = False,
        prefix:     str  = '',
        indentsymb: str  = '    ',
        branchsymb: str  = '  |____',
        depth:      int  = 0
    ) -> Generator[str, None, None]:
        if not isinstance(path, str):
            depth = 0;
            children = self.getHeadPaths();
        else:
            anon = anon or getAttribute(self.anon, path, expectedtype=bool, default=False);
            yield '{prefix}{tab}{branchsymb} {path}'.format(
                prefix = prefix,
                tab = indentsymb*(depth if depth == 0 else depth - 1),
                branchsymb = '' if depth == 0 else branchsymb,
                path = '########' if anon else path,
            );
            depth = depth + 1;
            children = [];
            if path in self.paths:
                children = [ v for u, v in self.docEdges if u == path ];
        for subpath in children:
            yield from self.documentStructurePretty(subpath, anon=anon, prefix=prefix, indentsymb=indentsymb, branchsymb=branchsymb, depth=depth);
        return;

    def documentStamp(self, depth: int = 0, start: bool = True) -> TranspileBlock:
        return TranspileBlock(
            kind       = 'code',
            content    = '____printfilestamp(depth={depth}, start={start});'.format(depth=depth, start=start),
            level      = 0,
            indentsymb = self.indentsymb
        );

    def documentTree(self, seed: Union[int, None]) -> TranspileBlock:
        return TranspileBlock(
            kind       = 'text:comment',
            lines      = formatTextBlockAsList(
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
                %% DOCUMENT-RANDOM-SEED: {}
                %% ********************************************************************************
                '''.format(seed if isinstance(seed, int) else '---')
            ) + [ '' ],
            level      = 0,
            indentsymb = self.indentsymb,
        );

    def generateCode(
        self,
        offset:     int       = 0,
        preambles:  List[str] = [],
        globalvars: List[str] = []
    ) -> Generator[str, None, None]:
        ## generate universal reference function
        yield '{tab}# universal reference function for files'.format(tab=self.tab(offset));
        yield '{tab}def {label}(path: str):'.format(
            tab   = self.tab(offset),
            label = self.schemes['file'],
        );
        for path in self.paths:
            yield '{tab}    if path == \'{path}\':'.format(
                tab  = self.tab(offset),
                path = path,
            );
            yield '{tab}        {label}();'.format(
                tab = self.tab(offset),
                path = path,
                label = self.getFunctionName(path),
            );
            yield '{tab}        return;'.format(tab = self.tab(offset));
        yield '{tab}    raise Exception(\'{msg}\'.format(path));'.format(
            msg = r'[\033[91;1mERROR\033[0m] Could not find a method associated to the document path \033[1m{}\033[0m.',
            tab = self.tab(offset),
        );

        ## generate function for preamble parts
        for name, blocks in self.preamble.items():
            yield '';
            yield '{tab}# preamble function \'{name}\''.format(tab=self.tab(offset), name=name)
            yield '{tab}def {label}():'.format(
                tab   = self.tab(offset),
                label = '{label}_{name}'.format(label=self.schemes['pre'], name=name),
            );
            yield from blocks.generateCode(offset=offset+1);
            yield '{tab}return'.format(tab=self.tab(offset + 1));

        ## generate individual functions for documents
        for document in self.documents.values():
            yield '';
            yield from document.generateCode(offset=offset, globalvars=globalvars, anon=self.isAnon(path));

        ## generate main function, which calls head functions first
        yield '';
        yield '{tab}# generate content from all files'.format(tab=self.tab(offset));
        yield '{tab}def {label}():'.format(
            tab   = self.tab(offset),
            label = self.schemes['main'],
        );
        yield '{tab}____cleardocument();'.format(tab=self.tab(offset + 1));
        for name in preambles:
            yield '{tab}{label}();'.format(
                tab   = self.tab(offset + 1),
                label = '{label}_{name}'.format(label=self.schemes['pre'], name=name),
            );
        for path in self.getHeadPaths():
            yield '{tab}{label}(\'{path}\');'.format(
                tab   = self.tab(offset + 1),
                label = self.schemes['file'],
                path  = path
            );
        yield '{tab}return;'.format(tab=self.tab(offset + 1));
        return;
