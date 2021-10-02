#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations

from src.local.misc import *;
from src.local.typing import *;

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
        indentsymb: str = '    '
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
    def content(self) -> Generator[str, None, None]:
        if hasattr(self, '_content'):
            yield '{tab}{line}'.format(
                tab = self.indentsymb*self.indentlevel,
                line = self._content
            );
        else:
            yield from formatBlockIndent(self.lines, indent=self.indentsymb*self.indentlevel);

    def generateCode(self, offset: int = 0) -> Generator[str, None, None]:
        indentlevel_orig = self.indentlevel;
        self.indentlevel += offset;
        if self.kind == 'text':
            yield from self.content;
        elif self.kind == 'text:linebreak':
            yield '{tab}print(\'\'\'\\n\'\'\');'.format(tab=self.indentsymb*self.indentlevel);
        elif self.kind == 'text:subst':
            line = '{tab}print(\'\'\'{expr}\'\'\'.format('.format(
                tab  = self.indentsymb*self.indentlevel,
                expr = '\n'.join(list(self.content)),
            )
            yield line + ('));' if len(self.subst) == 0 else '');
            for key, value in self.subst.items():
                indentlevel = value.indentlevel;
                value_lines = formatBlockIndent(value.lines, indent=self.indentsymb*(self.indentlevel + 2));
                value_lines[0] = re.sub(r'^\s*(.*)$', r'\1', value_lines[0]);
                yield '{tab}\'{key}\': {value},'.format(
                    tab = self.indentsymb*(self.indentlevel + 1),
                    key = key,
                    value = '\n'.join(value_lines),
                );
                value.indentlevel = indentlevel;
            if len(self.subst) > 0:
                yield '{tab});'.format(tab=self.indentsymb*self.indentlevel);
        elif self.kind == 'code':
            yield from self.content;
        elif self.kind == 'code:value':
            yield from self.content;
        elif re.match(r'^code:set', self.kind):
            yield '{tab}{varname} = {value};'.format(
                tab = self.indentsymb*self.indentlevel,
                **self.parameters
            );
        elif self.kind == 'code:escape':
            yield '{tab}pass;'.format(tab=self.indentsymb*self.indentlevel);
        elif self.kind == 'code:escape:1':
            yield '{tab}pass;'.format(tab=self.indentsymb*self.indentlevel);
        elif self.kind == 'code:input':
            pass;
        elif self.kind == 'code:input:anon':
            pass;
        elif self.kind == 'code:bib':
            pass;
        elif self.kind == 'code:bib:anon':
            pass;
        self.indentlevel = indentlevel_orig;
        return;
