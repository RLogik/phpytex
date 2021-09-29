#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

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
    def content(self) -> str:
        if hasattr(self, '_content'):
            return self._content;
        indent = self.indentsymb*self.indentlevel;
        lines = formatBlockIndent(self.lines, indent=indent);
        return '\n'.join(lines);

    def generateCode(self) -> Generator[str, None, None]:
        indent = self.indentsymb*self.indentlevel;
        if self.kind == 'text':
            yield self.content;
        elif self.kind == 'text:linebreak':
            yield '{tab}print(\'\'\'\\n\'\'\');'.format(tab=indent);
        elif self.kind == 'text:subst':
            line = '{tab}print(\'\'\'{expr}\'\'\'.format('.format(
                tab  = indent,
                expr = self.content,
            )
            yield line + ('));' if len(self.subst) == 0 else '');
            for key, value in self.subst.items():
                indentlevel = value.indentlevel;
                value_lines = formatBlockIndent(value.lines, indent=indent + self.indentsymb*2);
                value_lines[0] = re.sub(r'^\s*(.*)$', r'\1', value_lines[0]);
                yield '{tab}\'{key}\': {value},'.format(
                    tab = indent + self.indentsymb,
                    key = key,
                    value = '\n'.join(value_lines),
                );
                value.indentlevel = indentlevel;
            if len(self.subst) > 0:
                yield '{tab});'.format(tab=indent);
            return;
        elif self.kind == 'code':
            yield self.content;
        elif self.kind == 'code:value':
            yield self.content;
        elif self.kind == 'code:set':
            yield '{tab}{varname} = {value};'.format(
                tab = indent,
                **self.parameters
            );
        elif self.kind == 'code:escape':
            yield '{tab}pass;'.format(tab=indent);
            return;
        elif self.kind == 'code:escape:1':
            yield '{tab}pass;'.format(tab=indent);
            return;
        elif self.kind == 'code:input':
            return;
        elif self.kind == 'code:input:anon':
            return;
        elif self.kind == 'code:bib':
            return;
        elif self.kind == 'code:bib:anon':
            return;
        return;
