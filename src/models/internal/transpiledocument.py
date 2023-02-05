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
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile document
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileDocument(TokenisationDocument):
    blocks: TranspileBlocks;
    path_folder: str;

    def __init__(self, *_, **__):
        super(TokenisationDocument, self).__init__(*_, **__);
        self.path_folder = os.path.dirname(self.path) or '.';
        return;

    def __len__(self) -> int:
        return len(self.blocks);

    def __iter__(self) -> Generator[TranspileBlock, None, None]:
        for block in self.blocks:
            yield block;

    def tab(self, offset: int = 1) -> str:
        return self.indent_symbol * offset;

    # relativises a path relative to directory to a path relative to root
    def relativisePath(self, path: str):
        if os.path.isabs(path):
            if path.startswith(self.root):
                path = os.path.relpath(path=path, start=self.root);
        else:
            path = os.path.join(self.path_folder, path);
            path = os.path.relpath(path=path, start=self.root);
        return path;

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
        yield f'{self.tab(offset)}# generate content from file \'{self.path}\'';
        yield f'{self.tab(offset)}def {self.label}():';
        offset += 1;
        yield from TranspileBlock(
            kind = 'code',
            lines = [
                'global {name};'.format(name=name)
                for name in unique([ '__ROOT__', '__DIR__', '__FNAME__', '__ANON__', '__HIDE__', '__IGNORE__' ] + globalvars)
                if not name in [ '__STATE__' ]
            ] + [
                '__ROOT__ = \'.\';',
                f'__DIR__ = \'{self.path_folder}\';',
                f'__FNAME__ = \'{self.path}\';',
                '__IGNORE__ = False;',
                f'__ANON__ = {anon};',
                f'__HIDE__ = {hide};',
                '# Save current state locally. Use to restore state after importing subfiles.',
                '__STATE__ = (__ROOT__, __DIR__, __FNAME__, __ANON__, __HIDE__, __IGNORE__);',
            ]
        ).generateCode(offset, anon=False, hide=False);
        for block in self.blocks:
            yield from block.generateCode(offset, anon=anon, hide=hide);
        yield f'{self.tab(offset)}return;';
        return;
