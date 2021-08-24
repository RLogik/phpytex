#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;
import re;
from lark import Lark;
from lark import Tree;
from typing import List;
from typing import Union;
from textwrap import dedent;

from src.core.utils import readTextFile;
from src.core.utils import escapeForPython;
from src.core.utils import formatBlockIndent;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INDENTCHAR: str = '    ';
INDENTCHAR_RE: str = '    ';
INDENTLEVEL: int = 0;

# generate lexer via LARK:
PATH_GRAMMAR: str = 'src/grammars/phpytex.lark';
LEXER = Lark(readTextFile(PATH_GRAMMAR, internal=True), start='blocks', regex=True);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHODS string -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parseText(u: str) -> str:
    try:
        if u.strip() == '':
            return '';
        lines = lexedToBlocks(LEXER.parse(u));
    except:
        raise Exception('Could not parse input!');
    return lines;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PRIVATE METHODS: recursive lex -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToBlocks(u: Tree) -> str:
    global INDENTLEVEL;
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'blocks':
        INDENTLEVEL = 0;
        return ''.join([ lexedToBlock(child) for child in children ]);
    raise Exception('Could not parse expression!');

def lexedToBlock(u: Tree, indentoffset: str = '') -> str:
    global INDENTLEVEL;
    indentlevel = INDENTLEVEL;

    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'newlines':
        lines = lexedToStr(u.children[0]);
        n = len(re.findall(r'\n', lines));
        n = max(n-1, 0);
        if n == 0:
            return '';
        return '{tab}print(\'{newlines}\');\n'.format(
            tab = INDENTCHAR*INDENTLEVEL,
            newlines = '\\n'*n,
        );
    elif typ == 'block':
        return lexedToBlock(children[0]);
    ## QUICK COMMAND
    elif typ == 'blockquick':
        return lexedToBlock(children[0]);
    elif typ == 'quickset':
        varname = lexedToStr(children[0]);
        value = lexedToStr(children[1]);
        return '{x} = {val};\n'.format(x=varname, val=value);
    elif typ == 'quickescape':
        INDENTLEVEL = 0;
        return 'pass;\n';
    elif typ == 'quickescapeonce':
        INDENTLEVEL = max(indentlevel-1, 0);
        return '{tab}pass;\n'.format(tab=INDENTCHAR*INDENTLEVEL);
    ## INLINE SUBST
    elif typ == 'blockinline':
        expr = '';
        subst = [];
        i = 0;
        for child in children:
            if child.data == 'content':
                INDENTLEVEL = indentlevel;
                subexpr = lexedToBlock(child);
                expr += subexpr;
            elif child.data == 'codeinline':
                INDENTLEVEL = indentlevel + 1
                subexpr = lexedToBlock(child);
                subsubexpr = subexpr.split('\n');
                subexprs = [];
                for subexpr in subsubexpr:
                    if re.match(r'^\s*\#', subexpr):
                        continue;
                    subexpr = re.sub(r'^(.*);\s*$',  r'\1', subexpr);
                    subexpr = re.sub(r'^(.*\S)\s+$', r'\1', subexpr);
                    subexprs.append(subexpr);
                if len(subexprs) == 0:
                    continue;
                subexpr = '\n'.join(subexprs);
                expr += '{{{}}}'.format(i);
                subst.append(subexpr);
                i += 1;
        INDENTLEVEL = indentlevel;
        lines = [];
        if len(subst) == 0:
            lines.append('{tab}print(\'\'\'{expr}\'\'\'.format());'.format(
                tab  = INDENTCHAR*INDENTLEVEL,
                expr = expr,
            ))
        else:
            lines.append('{tab}print(\'\'\'{expr}\'\'\'.format('.format(
                tab  = INDENTCHAR*INDENTLEVEL,
                expr = expr,
            ));
            for s in subst:
                lines.append('{},'.format(s));
            lines.append('{tab}));'.format(tab = INDENTCHAR*INDENTLEVEL));
        line = '\n'.join(lines);
        return '{line}\n'.format(line=line);
    elif typ == 'content':
        expr = escapeForPython(lexedToStr(u));
        return expr;
    elif typ == 'codeinline':
        expr = formatBlockIndent(lexedToStr(children[0]), indent=INDENTCHAR*INDENTLEVEL);
        return expr;
    ## CODE BLOCK
    elif typ == 'blockcode':
        assert len(children) in [2, 4];
        if len(children) == 2:
            indentoffset = '';
            indentoffset_close = '';
            instructions = children[0];
            insidecode = children[1];
        else:
            indentoffset = lexedToStr(children[0]);
            indentoffset_close = lexedToStr(children[3]);
            instructions = children[1];
            insidecode = children[2];
        assert indentoffset == indentoffset_close, 'Inconsistent indentation for code block.';
        assert instructions.data == 'python', 'Currently only accepts code blocks of python type.';
        line = lexedToBlock(insidecode, indentoffset=indentoffset);
        return '{line}\n'.format(line=line);
    elif typ == 'insidecode':
        lines = '\n'.join([ indentoffset + INDENTCHAR + '.' ] + [ lexedToStr(child) for child in children ]);
        lines = dedent(lines).split('\n')[1:];
        for line in lines:
            INDENTLEVEL = getIndentationLevel(line, INDENTCHAR);
            if re.match(r'^.*:\s*$', line):
                INDENTLEVEL += 1;
        return '\n'.join(lines);
    raise Exception('Could not parse expression!');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS: filtration
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToStr(u: Union[str, Tree]) -> str:
    if isinstance(u, str):
        return str(u);
    return ''.join([ lexedToStr(uu) for uu in u.children ]);

def filterSubexpr(u: Tree) -> List[Tree]:
    return [uu for uu in u.children if isinstance(uu, Tree) and hasattr(uu, 'data') and not uu.data == 'noncapture'];

def filterOutNoncapture(u: Tree) -> List[Union[str, Tree]]:
    return [uu for uu in u.children if not isinstance(uu, Tree) or ( hasattr(uu, 'data') and not uu.data == 'noncapture' ) ];

def getIndentationLevel(u: str, tab: str) -> int:
    n = 0;
    while True:
        if not u.startswith(tab*(n+1)):
            break;
        n += 1;
    return n;

# --------------------------------------------------------------------------------
# CLASS: indentation tracker
# --------------------------------------------------------------------------------

class IndentationTracker(object):
    pattern: str = r'    ';
    reference: int = 0;
    start: int = 1;
    last: int = 1;

    def __init__(self, pattern = None):
        if isinstance(pattern, str):
            self.pattern = pattern;
        return;

    def reset(self):
        self.reference = 0;
        self.start     = 1;
        self.last      = 1;

    def computeIndentations(self, s: str, pattern = None) -> int:
        pattern = pattern if isinstance(pattern, str) else self.pattern;
        return len(re.findall(pattern, s));

    def initOffset(self, s: str):
        self.reset();
        self.reference = self.computeIndentations(s);

    def computeOffset(self, s: str):
        return max(self.computeIndentations(s) - self.reference, 1);

    def setOffset(self, s: str):
        self.last = self.computeOffset(s);

    def decrOffset(self):
        self.last = max(self.last - 1, 1);

    def incrOffset(self):
        self.last = self.last + 1;