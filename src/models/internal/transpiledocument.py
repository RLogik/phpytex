#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.core.utils import *;
from src.models.generated.tokenisation import *;
from src.models.internal.transpileblock import *;
from src.models.internal.transpileblocks import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'TranspileDocument',
    'path_relative_to_root',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile document
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileDocument(TokenisationDocument):
    blocks: TranspileBlocks;

    def __init__(self, *_, **__):
        super().__init__(*_, **__);
        self.blocks = TranspileBlocks();
        return;

    @property
    @final_property
    def path_dir(self) -> str:
        '''
        Absolute path to directory in which the document finds itself.
        '''
        return os.path.dirname(self.path);

    def __len__(self) -> int:
        return len(self.blocks);

    def __iter__(self) -> Generator[TranspileBlock, None, None]:
        yield from self.blocks;

    def append(self, block: TranspileBlock):
        self.blocks.append(block);
        return;

    def generateCode(
        self,
        offset:     int       = 0,
        globalvars: list[str] = [],
        anon:       bool      = False,
        hide:       bool      = False,
    ) -> Generator[str, None, None]:
        yield from TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            lines = [
                f'# generate content from file \'{self.path}\'',
                f'def {self.label}():',
            ],
        ).generateCode(offset, anon=False, hide=False);
        yield from TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            lines = [
                'global {name};'.format(name=name)
                for name in unique([ '__ROOT__', '__DIR__', '__FNAME__', '__ANON__', '__HIDE__', '__IGNORE__' ] + globalvars)
                if not name in [ '__STATE__' ]
            ] + [
                '__ROOT__ = \'.\';',
                f'__DIR__ = \'{self.path_dir}\';',
                f'__FNAME__ = \'{self.path}\';',
                '__IGNORE__ = False;',
                f'__ANON__ = {anon};',
                f'__HIDE__ = {hide};',
                '# Save current state locally. Use to restore state after importing subfiles.',
                '__STATE__ = (__ROOT__, __DIR__, __FNAME__, __ANON__, __HIDE__, __IGNORE__);',
            ],
        ).generateCode(offset+1, anon=False, hide=False);
        for block in self:
            yield from block.generateCode(offset+1, anon=anon, hide=hide);
        yield from TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            lines = [
                'return;',
            ],
        ).generateCode(offset, anon=False, hide=False);
        return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OTHER METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def path_relative_to_root(
    path: str,
    document: TranspileDocument,
) -> str:
    '''
    If a path is expressed within a document,
    this method allows one to re-express the path
    relative to the project root if possible.

    @inputs
    - `path` - `<str>` path.
    - `document` - a `TranspileDocument`-instance

    @returns
    Path relativised to root, if not absolute or if a subpath of root.

    ## Cases ##

    1. `path` is absolute. Then the path will be relativised to root,
      if and only if `path` is a subpath of the root.
    2. `path` is relative. Then it is assumed that _this_ is relative
      to the directory in which the document finds itself.
      This is taken into account, in order to re-relativise the path
      with respect to the project root.
    '''
    if os.path.isabs(path):
        # relativise with respect to root if path is subpath of the root:
        if path.startswith(document.root):
            path = os.path.relpath(path=path, start=document.root);
    else:
        # re-relativise if not absolute:
        path = os.path.join(document.path_dir, path);
        path = os.path.relpath(path=path, start=document.root);
    return path;
