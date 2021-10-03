#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.local.misc import *;
from src.local.typing import *;

from src.core.utils import escapeForPython;
from src.core.utils import formatBlockIndent;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile block
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileBlock(object):
    kind: str;
    _content: str;
    lines: List[str];
    indentlevel: int;
    indentsymb: str;
    parameters: Dict[str, Any];
    subst: Dict[str, TranspileBlock];

    def __init__(self,
        kind: str,
        content: Any = None,
        lines: List[str] = [],
        indentlevel: int = 0,
        indentsymb: str = '    ',
        **_
    ):
        self.lines = lines;
        self.kind = kind;
        self.indentlevel = indentlevel;
        self.indentsymb = indentsymb;
        self.parameters = dict();
        self.subst = dict();
        if isinstance(content, str):
            self._content = content;
        return;

    @property
    def isCode(self) -> bool:
        return True if re.match(r'^code(:|$)', self.kind) else False;

    @property
    def content(self) -> Generator[str, None, None]:
        tab = self.tab() if self.isCode else '';
        if hasattr(self, '_content'):
            yield '{tab}{line}'.format(tab = tab, line = self._content);
        else:
            yield from formatBlockIndent(self.lines, indent=tab);

    def tab(self, delta: int = 0) -> str:
        return self.indentsymb * (self.indentlevel + delta);

    def generateCode(self, offset: int = 0) -> Generator[str, None, None]:
        state = dict(indentlevel=self.indentlevel, indentsymb=self.indentsymb);
        self.indentlevel += offset;
        if self.kind == 'text:linebreak':
            yield '{tab}print(\'\'\'\\n\'\'\');'.format(tab=self.tab());
        elif self.kind == 'text' or re.match(r'^text:comment', self.kind):
            for line in self.content:
                yield '{tab}print(\'\'\'{expr}\'\'\');'.format(
                    tab  = self.tab(),
                    expr = escapeForPython(line, withformatting=False),
                );
        elif self.kind == 'text:subst':
            line = '{tab}print(\'\'\'{expr}\'\'\'.format('.format(
                tab  = self.tab(),
                expr = '\n'.join(list(self.content)),
            )
            yield line + ('));' if len(self.subst) == 0 else '');
            for key, value in self.subst.items():
                indentlevel = value.indentlevel;
                value_lines = formatBlockIndent(value.lines, indent=self.tab(2));
                value_lines[0] = re.sub(r'^\s*(.*)$', r'\1', value_lines[0]);
                yield '{tab}{key} = {value},'.format(
                    tab = self.tab(1),
                    key = key,
                    value = '\n'.join(value_lines),
                );
                value.indentlevel = indentlevel;
            if len(self.subst) > 0:
                yield '{tab}));'.format(tab=self.tab());
        elif self.kind in [ 'code', 'code:import', 'code:value']:
            yield from self.content;
        elif re.match(r'^code:set', self.kind):
            line = '{varname} = {codevalue};'.format(**self.parameters);
            block = TranspileBlock(kind='code', content=line, **state);
            yield from block.generateCode(offset=offset);
        elif re.match(r'^code:escape', self.kind):
            block = TranspileBlock(kind='code', content='pass;', **state);
            yield from block.generateCode(offset=offset);
        elif self.kind == 'code:input':
            pass;
        elif self.kind == 'code:input:anon':
            pass;
        elif self.kind == 'code:bib':
            pass;
        elif self.kind == 'code:bib:anon':
            pass;
        self.indentlevel = state['indentlevel'];
        return;

class TranspileBlocks(object):
    blocks: List[TranspileBlock];

    def __init__(self, blocks: List[TranspileBlock] = []):
        self.blocks = blocks[:];

    def __len__(self) -> int:
        return len(self.blocks);

    def __iter__(self) -> Generator[TranspileBlock, None, None]:
        for block in self.blocks:
            yield block;
        return;

    def append(self, block: TranspileBlock):
        self.blocks.append(block);

    def generateCode(self, offset: int = 0) -> Generator[str, None, None]:
        for block in self.blocks:
            yield from block.generateCode(offset=offset);
        return;
