#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.code import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.core.log import *;
from src.core.utils import *;
from src.models.generated.tokenisation import *;
from src.models.config import *;
from src.models.internal.dictionaries import *;
from src.models.internal.graphs import *;
from src.models.internal.transpileblock import *;
from src.models.internal.transpileblocks import *;
from src.models.internal.transpiledocument import *;


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'TranspileDocuments',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile documents
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class TranspileDocuments(TokenisationDocuments):
    documents: dict[str, TranspileDocument] = field(init=False, default_factory=dict);
    preamble: dict[str, TranspileBlocks] = field(init=False, default_factory=dict);

    anon: DictionaryWithDefault[str, bool] = field(init=False, default_factory=factory_dictionary_str_bool_false);
    hide: DictionaryWithDefault[str, bool] = field(init=False, default_factory=factory_dictionary_str_bool_false);
    variables: dict[str, Any] = field(init=False, default_factory=dict);

    paths: list[str] = field(init=False, default_factory=list);
    edges: list[tuple[str, str]] = field(init=False, default_factory=list);
    docEdges: list[tuple[str, str]] = field(init=False, default_factory=list);

    def __len__(self) -> int:
        return len(self.documents);

    def __iter__(self) -> Generator[TranspileDocument, None, None]:
        for _, document in self.documents.items():
            yield document;

    def evaluate(self, codevalue: str, document: TranspileDocument):
        localvariables = self.variables | document.variables | {
            '__ROOT__': os.path.abspath(document.root),
            '__DIR__': os.path.abspath(document.pathfolder),
        };
        return eval(codevalue, None, localvariables);

    @property
    @final_property
    def head_paths(self) -> list[str]:
        '''
        **WARNING:** only call this property after _all_ paths have been added!
        '''
        return get_roots_graph(nodes=self.paths, edges=self.edges);

    def subpaths(self, path: str) -> list[str]:
        return [ __ for _, __ in self.edges if _ == path ];

    def function_name(self, path: str) -> str:
        try:
            index = self.paths.index(path);
        except:
            index = None;
        return f'{self.name_space.function_name_file}_{index}';

    def addPreamble(self, name: str, blocks: TranspileBlocks):
        self.preamble[name] = blocks;
        return;

    def addDocument(self, path: str):
        if path in self.paths:
            return;
        self.paths.append(path);
        document = TranspileDocument(
            root = self.root,
            path = os.path.relpath(path=os.path.abspath(path), start=self.root),
            indent_symbol = self.indent_symbol,
            label = self.function_name(path)
        );
        self.documents[path] = document;
        # update properites of anonymity and hidden-state:
        property_inheritance_graph(edges=self.edges, state=self.anon);
        property_inheritance_graph(edges=self.edges, state=self.hide);
        return;

    def addBlocks(self, path: str, blocks: TranspileBlocks):
        assert path in self.documents, 'Must add document first, before adding blocks.';
        document = self.documents[path];
        for block in blocks:
            state = dict(level=block.level, indent_symbol=block.indent_symbol);
            if re.match(r'^text($|:)', block.kind):
                document.append(block);
            elif block.kind == 'code':
                document.append(block);
            elif block.kind == 'code:escape':
                document.append(block);
            elif block.kind == 'code:set':
                variable_name   = block.parameters.var_name;
                variable_value = block.parameters.code_value;
                scope     = block.parameters.scope;
                try:
                    value = self.evaluate(variable_value, document=document);
                except:
                    ## TODO: deal with error
                    log_error(f'Could not evaluate \033[1m<<< {scope} set {variable_name} = {variable_value} >>>\033[0m.');
                    continue;
                if scope == 'local':
                    document.variables[variable_name] = value;
                elif scope == 'global':
                    self.variables[variable_name] = value;
                document.append(block);
            elif block.kind == 'code:input':
                ## extract block parameters:
                _path      = block.parameters.path;
                anon       = block.parameters.anon;
                hide       = block.parameters.hide;
                mode       = block.parameters.mode;
                textindent = block.parameters.tab;
                ## unpack path expression (potentially evaluate):
                try:
                    _path = self.evaluate(_path, document=document);
                except:
                    ## TODO: deal with error
                    cmd  = ('bibliography' if mode == 'bib' else 'input') \
                            + ('_anon' if anon else ('_hide' if hide else ''));
                    log_error(f'Could not evaluate \033[1m<<< {cmd} {_path}\033[0m >>>\033[0m.');
                    continue;
                _path = path_relative_to_root(path=_path, document=document);
                ## add edge for the sake of display (regardless of whether input or bib mode):
                self.docEdges.append((path, _path));
                if mode == 'input':
                    self.edges.append((path, _path));
                # update properites of anonymity and hidden-state:
                property_inheritance_graph(edges=self.edges, state=self.anon, force=[_path] if anon else []);
                property_inheritance_graph(edges=self.edges, state=self.hide, force=[_path] if hide else []);
                ## create phpytex-code blocks based on computed path:
                if mode == 'input':
                    document.append(TranspileBlock(kind='text:empty', **state)); # force empty line before input of file
                    document.append(TranspileBlock(
                        kind        = 'code',
                        lines       = [
                            f'{self.name_space.function_name_file}(\'{_path}\');',
                            '# Restore state of current file:',
                            '__ROOT__, __DIR__, __FNAME__, __ANON__, __HIDE__, __IGNORE__ = __STATE__;',
                        ],
                        **state
                    ));
                elif mode == 'bib':
                    document.append(TranspileBlock(
                        kind           = 'code',
                        lines          = [
                            f'____insertbib(\'{_path}\', textindent=\'{textindent}\', anon={anon});',
                        ],
                        **state
                    ));
        document.append(TranspileBlock(kind='text:empty', level=0, indent_symbol=self.indent_symbol)); # force empty add end of file
        return;

    def documentStructurePretty(
        self,
        path = None,
        anon:       bool = False,
        prefix:     str  = '',
        indent_symbol: str  = '    ',
        branchsymb: str  = '  |____',
        depth:      int  = 0
    ) -> Generator[str, None, None]:
        if not isinstance(path, str):
            depth = 0;
            children = self.head_paths;
        elif self.hide[path]:
            return;
        else:
            anon = anon or self.anon[path];
            yield '{prefix}{tab}{branchsymb} {path}'.format(
                prefix = prefix,
                tab = indent_symbol*(depth if depth == 0 else depth - 1),
                branchsymb = '' if depth == 0 else branchsymb,
                path = '########' if anon else path,
            );
            depth = depth + 1;
            children = [];
            if path in self.paths:
                children = [ v for u, v in self.docEdges if u == path ];
        for subpath in children:
            yield from self.documentStructurePretty(subpath, anon=anon, prefix=prefix, indent_symbol=indent_symbol, branchsymb=branchsymb, depth=depth);
        return;

    def documentStamp(self, depth: int, start: bool, anon: bool, hide: bool) -> TranspileBlock:
        return TranspileBlock(
            kind       = 'code',
            content    = f'____printfilestamp(depth={depth}, start={start}, anon={anon}, hide={hide});',
            level      = 0,
            indent_symbol = self.indent_symbol
        );

    def documentTree(self, seed: Optional[int]) -> TranspileBlock:
        return TranspileBlock(
            kind       = 'text:comment',
            lines      = dedent_as_list(
                '''
                %% ********************************************************************************
                %% DOCUMENT STRUCTURE:
                %% ~~~~~~~~~~~~~~~~~~~
                %%
                '''
            ) \
            + list(self.documentStructurePretty(prefix='%% ')) \
            + dedent_as_list(
                f'''
                %%
                %% DOCUMENT-RANDOM-SEED: {seed if isinstance(seed, int) else "---"}
                %% ********************************************************************************
                '''
            ) \
            + [ '' ],
            level      = 0,
            indent_symbol = self.indent_symbol,
        );

    def generateCode(
        self,
        offset:     int       = 0,
        preambles:  list[str] = [],
        globalvars: list[str] = [],
    ) -> Generator[str, None, None]:
        tab = self.indent_symbol;

        # generate universal reference function
        yield from TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            lines = dedent_as_list(
                f'''
                # universal reference function for files
                def {self.name_space.function_name_file}(path: str):
                {tab}match path:
                '''
            ) \
            + flatten([[
                f'{tab}{tab}case \'{path}\':',
                f'{tab}{tab}{tab}{self.function_name(path)}();',
            ] for path in self.paths]) \
            + [
                f'{tab}{tab}case _:'
                f'{tab}{tab}{tab}raise Exception(f\'[\\x1b[91;1mERROR\\x1b[0m] Could not find a method associated to the document {{path}}.\')'
                r' \033[1m{}\033[0m.'
            ] \
            + [
                f'{tab}return;',
            ],
            indent_symbol = self.indent_symbol,
        ).generateCode(offset=offset, anon=False, hide=False);

        # generate function for preamble parts
        for name, blocks in self.preamble.items():
            yield '';
            yield from TranspileBlock(
                lines = dedent_as_list(
                    f'''
                    # preamble function \'{name}\'
                    def {self.name_space.function_name_pre}_{name}():
                    '''
                ),
                indent_symbol = self.indent_symbol,
            ).generateCode(offset=offset, anon=False, hide=False);
            yield from blocks.generateCode(offset=offset+1, anon=False, hide=False);
            yield from TranspileBlock(
                lines = [
                    f'{tab}return;',
                ],
                indent_symbol = self.indent_symbol,
            ).generateCode(offset, anon=False, hide=False);

        # generate individual functions for documents
        for path, document in self.documents.items():
            yield '';
            yield from document.generateCode(
                offset = offset,
                globalvars = globalvars,
                anon = self.anon[path],
                hide = self.hide[path],
            );

        # generate main function, which calls head functions first
        yield '';
        yield from TranspileBlock(
            lines = dedent_as_list(
                f'''
                # generate content from all files
                def {self.name_space.function_name_main}():
                {tab}____cleardocument();
                '''
             ) \
            + [
                f'{tab}{self.name_space.function_name_pre}_{name}();'
                for name in preambles
            ] \
            + [
                f'{tab}{self.name_space.function_name_file}(\'{path}\');'
                for path in self.head_paths
            ] \
            + [
                f'{tab}return;',
            ],
            indent_symbol = self.indent_symbol,
        ).generateCode(offset=offset, anon=False, hide=False);
        return;
