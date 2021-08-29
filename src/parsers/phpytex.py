#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
from lark import Lark;
from lark import Tree;
from typing import List;
from typing import Union;
from textwrap import dedent;

from src.core.utils import formatBlockIndent;
from src.setup.methods import getGrammar;
from src.parsers.methods import escapeForPython;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_indent_char: str = '    ';
_indent_char_re: str = '    ';
_indent_level: int = 0;
_lexer = None;

def getLexer() -> Lark:
    global _lexer;
    if not isinstance(_lexer, Lark):
        _lexer = Lark(getGrammar('phpytex.lark'), start='blocks', regex=True);
    return _lexer;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHODS string -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parseText(u: str) -> str:
    try:
        if u.strip() == '':
            return '';
        lines = lexedToBlocks(getLexer().parse(u));
    except:
        raise Exception('Could not parse input!');
    return lines;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PRIVATE METHODS: recursive lex -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToBlocks(u: Tree) -> str:
    global _indent_level;
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'blocks':
        _indent_level = 0;
        return ''.join([ lexedToBlock(child) for child in children ]);
    raise Exception('Could not parse expression!');

def lexedToBlock(u: Tree, indentoffset: str = '') -> str:
    global _indent_level;
    indentlevel0 = _indent_level;

    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'newlines':
        lines = lexedToStr(u.children[0]);
        n = len(re.findall(r'\n', lines));
        n = max(n-1, 0);
        if n == 0:
            return '';
        return '{tab}print(\'{newlines}\');\n'.format(
            tab = _indent_char*_indent_level,
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
        _indent_level = 0;
        return 'pass;\n';
    elif typ == 'quickescapeonce':
        _indent_level = max(indentlevel0-1, 0);
        return '{tab}pass;\n'.format(tab=_indent_char*_indent_level);
    ## INLINE SUBST
    elif typ == 'blockinline':
        expr = '';
        subst = [];
        i = 0;
        for child in children:
            if child.data == 'content':
                _indent_level = indentlevel0;
                subexpr = lexedToBlock(child);
                expr += subexpr;
            elif child.data == 'codeinline':
                _indent_level = indentlevel0 + 1
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
        _indent_level = indentlevel0;
        lines = [];
        if len(subst) == 0:
            lines.append('{tab}print(\'\'\'{expr}\'\'\'.format());'.format(
                tab  = _indent_char*_indent_level,
                expr = expr,
            ))
        else:
            lines.append('{tab}print(\'\'\'{expr}\'\'\'.format('.format(
                tab  = _indent_char*_indent_level,
                expr = expr,
            ));
            for s in subst:
                lines.append('{},'.format(s));
            lines.append('{tab}));'.format(tab = _indent_char*_indent_level));
        line = '\n'.join(lines);
        return '{line}\n'.format(line=line);
    elif typ == 'content':
        expr = escapeForPython(lexedToStr(u));
        return expr;
    elif typ == 'codeinline':
        expr = formatBlockIndent(lexedToStr(children[0]), indent=_indent_char*_indent_level);
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
        lines = '\n'.join([ indentoffset + _indent_char + '.' ] + [ lexedToStr(child) for child in children ]);
        lines = dedent(lines).split('\n')[1:];
        for line in lines:
            _indent_level = getIndentationLevel(line, _indent_char);
            if re.match(r'^.*:\s*$', line):
                _indent_level += 1;
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
# METHOD: set indentation
# --------------------------------------------------------------------------------

def setIndentation(tabs: bool = False, spaces: int = 4, **_):
    global _indent_char;
    global _indent_char_re;
    if tabs:
        _indent_char = '\t';
        _indent_char_re = r'\t';
    else:
        _indent_char_re = _indent_char = ' '*spaces;
        _indent_char_re = _indent_char;
    return;
