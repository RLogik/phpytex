#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.core.utils import *;
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

@dataclass
class TranspileDocumentRaw:
    label: str = field();
    root: str = field();
    path: str = field();
    indentsymb: str = field();
    variables: dict[str, Any] = field(default_factory=dict);
    pathfolder: str = field(init=False)
    blocks: TranspileBlocks = field(init=False, default_factory=TranspileBlocks);

class TranspileDocument(TranspileDocumentRaw):
    def __init__(self, *_, **__):
        super(TranspileDocument, self).__init__(*_, **__);
        self.pathfolder = os.path.dirname(self.path) or '.';
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
        globalvars: list[str] = [],
        anon:       bool      = False,
        hide:       bool      = False,
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
                for name in unique([ '__ROOT__', '__DIR__', '__FNAME__', '__ANON__', '__HIDE__', '__IGNORE__' ] + globalvars)
                if not name in [ '__STATE__' ]
            ] + [
                '__ROOT__ = \'.\';'.format(),
                '__DIR__ = \'{path}\';'.format(path = self.pathfolder),
                '__FNAME__ = \'{path}\';'.format(path = self.path),
                '__IGNORE__ = False;',
                '__ANON__ = {};'.format(anon),
                '__HIDE__ = {};'.format(hide),
                '# Save current state locally. Use to restore state after importing subfiles.',
                '__STATE__ = (__ROOT__, __DIR__, __FNAME__, __ANON__, __HIDE__, __IGNORE__);',
            ]
        ).generateCode(offset + 1, anon=False, hide=False);
        for block in self.blocks:
            yield from block.generateCode(offset + 1, anon=anon, hide=hide);
        yield '{tab}return;'.format(tab=self.tab(offset + 1));
        return;
