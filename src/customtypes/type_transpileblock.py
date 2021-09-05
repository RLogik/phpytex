#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations

from typing import Any;
from typing import Dict;

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
    content: str;
    num_lines: int;
    indentlevel: int;
    indentchar: str;
    parameters: Dict[str, Any];
    subst: Dict[str, TranspileBlock];

    def __init__(self,
        kind: str,
        content: str = '',
        indentlevel: int = 0,
        indentchar: str = '    '
    ):
        self.kind = kind;
        self.indentlevel = indentlevel;
        self.indentchar = indentchar;
        self.content = content;
        return;

    def __str__(self) -> str:
        if self.kind == 'text':
            return self.content;
        elif self.kind == 'text:subst':
            lines = [];
            lines.append('{tab}print(\'\'\'{expr}\'\'\'.format('.format(
                tab  = self.indentchar*self.indentlevel,
                expr = self.content,
            ));
            for key, value in self.subst.items():
                value.indentlevel += 1;
                lines.append('{tab}\'{key}\': {value},'.format(
                    tab = self.indentchar*(self.indentlevel+1),
                    key = key,
                    value = str(value),
                ));
                value.indentlevel -= 1;
            return '\n'.join(lines);
        elif self.kind == 'code':
            pass;
        elif self.kind == 'code:inline':
            return formatBlockIndent(self.content, indent=self.indentchar*self.indentlevel);
        raise Exception('Unrecognised kind.');
