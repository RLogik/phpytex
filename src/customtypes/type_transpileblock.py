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
# CLASS transpile parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileBlockParameters(object):
    mode:      str;
    scope:     str;
    anon:      bool;
    hide:      bool;
    varname:   str;
    codevalue: str;
    keep:      bool;
    level:     int;
    path:      str;
    tab:       str;

    def __init__(
        self,
        mode:      str  = '',
        scope:     str  = '',
        anon:      bool = False,
        hide:      bool = False,
        varname:   str  = '',
        codevalue: str  = '',
        keep:      bool = True,
        level:     int  = 0,
        path:      str  = '',
        tab:       str  = '',
        **_
    ):
        self.mode      = mode;
        self.scope     = scope;
        self.anon      = anon;
        self.hide      = hide;
        self.varname   = varname;
        self.codevalue = codevalue;
        self.keep      = keep;
        self.level     = level;
        self.path      = path;
        self.tab       = tab;
        return;

    def asDict(self) -> Dict[str, Any]:
        return dict(
            mode      = self.mode,
            scope     = self.scope,
            anon      = self.anon,
            hide      = self.hide,
            varname   = self.varname,
            codevalue = self.codevalue,
            keep      = self.keep,
            level     = self.level,
            path      = self.path,
            tab       = self.tab,
        );
    pass;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS transpile block
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TranspileBlock(object):
    kind: str;
    _content: str;
    lines: List[str];
    level: int;
    indentsymb: str;
    parameters: TranspileBlockParameters;
    margin: str;
    subst: Dict[str, TranspileBlock];

    def __init__(self,
        kind:        str,
        content:     Any            = None,
        lines:       List[str]      = [],
        level: int            = 0,
        indentsymb:  str            = '    ',
        parameters:  Dict[str, Any] = dict(),
        margin: str = '',
        **_
    ):
        self.lines = lines;
        self.kind = kind;
        self.level = level;
        self.indentsymb = indentsymb;
        self.parameters = TranspileBlockParameters(**parameters);
        self.margin = margin;
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
            yield from formatBlockIndent(self.lines, indent=tab, unindent=False);

    def tab(self, delta: int = 0) -> str:
        return self.indentsymb * (self.level + delta);

    def generateCode(
        self,
        offset: int = 0,
        anon: bool = False,
        hide: bool = False,
        align: bool = False,
    ) -> Generator[str, None, None]:
        state = dict(level=self.level, indentsymb=self.indentsymb);
        self.level += offset;
        if self.kind == 'text:empty':
            yield '{tab}____print(\'\', anon={anon}, hide={hide}, align={align});'.format(
                tab   = self.tab(),
                anon  = anon,
                hide  = hide,
                align = align,
            );
        elif self.kind in [ 'text', 'text:comment' ]:
            for line in self.content:
                yield '{tab}____print(\'\'\'{expr}\'\'\', anon={anon}, hide={hide}, align={align});'.format(
                    tab  = self.tab(),
                    expr = escapeForPython(line, withformatting=False),
                    anon = anon,
                    hide = hide,
                    align = align,
                );
        elif self.kind == 'text:subst':
            if len(self.subst) == 0:
                yield '{tab}____print(\'\'\'{expr}\'\'\'.format(), anon={anon}, hide={hide}, align={align});'.format(
                    tab  = self.tab(),
                    expr = '\n'.join(list(self.content)),
                    anon = anon,
                    hide = hide,
                    align = align,
                );
            else:
                yield '{tab}__MARGIN__ = \'{margin}\';'.format(
                    tab = self.tab(),
                    margin = self.margin,
                );
                yield '{tab}____print(\'\'\'{expr}\'\'\'.format('.format(
                    tab  = self.tab(),
                    expr = '\n'.join(list(self.content)),
                );
                for key, value in self.subst.items():
                    level = value.level;
                    value_lines = formatBlockIndent(value.lines, indent=self.tab(2), unindent=True);
                    value_lines[0] = re.sub(r'^\s*(.*)$', r'\1', value_lines[0]);
                    yield '{tab}{key} = {value},'.format(
                        tab = self.tab(1),
                        key = key,
                        value = '\n'.join(value_lines),
                    );
                    value.level = level;
                yield '{tab}), anon={anon}, hide={hide}, align={align});'.format(
                    tab = self.tab(),
                    anon = anon,
                    hide = hide,
                    align = align,
                );
        elif self.kind in [ 'code', 'code:import', 'code:value']:
            yield from self.content;
        elif self.kind == 'code:set':
            line = '{varname} = {codevalue};'.format(**self.parameters.asDict());
            block = TranspileBlock(kind='code', content=line, **state);
            yield from block.generateCode(offset=offset, align=align);
        elif self.kind == 'code:escape':
            block = TranspileBlock(kind='code', content='pass;', **state);
            yield from block.generateCode(offset=offset, align=align);
        elif self.kind == 'code:input':
            pass;
        self.level = state['level'];
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

    def generateCode(
        self,
        offset: int  = 0,
        anon:   bool = False,
        hide:   bool = False,
        align:  bool = False,
    ) -> Generator[str, None, None]:
        for block in self.blocks:
            yield from block.generateCode(offset=offset, anon=anon, hide=hide, align=align);
        return;
