#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.types import *;

from src.models.internal.transpileblock import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'TranspileBlocks',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile blocks
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class TranspileBlocks():
    blocks: TranspileBlock = field(default_factory=list);

    def __len__(self) -> int:
        return self.blocks.__len__();

    def __iter__(self) -> Generator[TranspileBlock, None, None]:
        yield from self.blocks;

    def append(self, block: TranspileBlock):
        self.blocks.append(block);

    def generateCode(
        self,
        offset: int  = 0,
        anon: bool = False,
        hide: bool = False,
    ) -> Generator[str, None, None]:
        for block in self.blocks:
            yield from block.generateCode(offset=offset, anon=anon, hide=hide);
