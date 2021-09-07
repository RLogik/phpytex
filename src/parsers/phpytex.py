#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
import json;
from lark import Lark;
from lark import Tree;
from typing import Any;
from typing import Dict;
from typing import List;
from typing import Tuple;
from typing import Union;

from src.core.utils import lengthOfWhiteSpace;
from src.core.utils import formatBlockUnindent;
from src.setup.methods import getGrammar;
from src.parsers.methods import escapeForPython;
from src.customtypes.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_lexer = None;

def getLexer() -> Lark:
    global _lexer;
    if not isinstance(_lexer, Lark):
        _lexer = Lark(getGrammar('phpytex.lark'), start='blocks', regex=True);
    return _lexer;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHODS string -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parseText(u: str, indentation: IndentationTracker) -> List[TranspileBlock]:
    blocks = [];
    try:
        if not ( u.strip() == '' ):
            blocks = lexedToBlocks(getLexer().parse(u), indentation=indentation);
    except:
        raise Exception('Could not parse input!');
    return blocks;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PRIVATE METHODS: recursive lex -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToBlocks(u: Tree, indentation: IndentationTracker) -> List[TranspileBlock]:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'blocks':
        return [ lexedToBlock(child, indentation=indentation) for child in children ];
    raise Exception('Could not parse expression!');

def lexedToBlock(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'newlines':
        return TranspileBlock(kind='text:linebreak', indentlevel=indentation.last, indentchar=indentation.symb);
    ## TEXT CONTENT
    elif typ == 'blockcontent':
        return parseBlockContent(children, indentation=indentation);
    ## CODE BLOCK
    elif typ == 'blockcode':
        return parseBlockCode(children[0], indentation=indentation);
    ## QUICK COMMAND
    elif typ == 'blockquick':
        return parteBlockQuickCommand(children[0], indentation=indentation);
    raise Exception('Could not parse expression!');

## BLOCK PARSERS

def parseBlockContent(children: List[Tree], indentation: IndentationTracker) -> TranspileBlock:
    exprs = [];
    subst: Dict[str, TranspileBlock] = dict();
    i = 0;
    for child in children:
        if child.data == 'textcontent':
            text = escapeForPython(lexedToStr(child));
            exprs.append(text);
        elif child.data == 'codeinline':
            key = 'subst' +  str(i);
            subblock = parseCodeInline(child, indentation=indentation);
            subst[key] = subblock;
            exprs.append('{{{}}}'.format(key));
            i += 1;
    expr = ''.join(exprs);
    block = TranspileBlock(kind='text:subst', content=expr, indentlevel=indentation.last, indentchar=indentation.symb);
    block.subst = subst;
    return block;

def parteBlockQuickCommand(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'quickset':
        varname = lexedToStr(children[0]);
        value = lexedToStr(children[1]);
        return TranspileBlock(kind='code:set', content='{x} = {val};'.format(x=varname, val=value), indentlevel=indentation.last, indentchar=indentation.symb);
    elif typ == 'quickinput':
        path = lexedToStr(children[0]);
        return TranspileBlock(kind='code:input', content=path, indentlevel=indentation.last, indentchar=indentation.symb);
    elif typ == 'quickinput_anon':
        path = lexedToStr(children[0]);
        return TranspileBlock(kind='code:input:anon', content=path, indentlevel=indentation.last, indentchar=indentation.symb);
    elif typ == 'quickbib':
        path = lexedToStr(children[0]);
        return TranspileBlock(kind='code:bib', content=path, indentlevel=indentation.last, indentchar=indentation.symb);
    elif typ == 'quickbib_anon':
        path = lexedToStr(children[0]);
        return TranspileBlock(kind='code:bib:anon', content=path, indentlevel=indentation.last, indentchar=indentation.symb);
    elif typ == 'quickescape':
        indentation.last = 1;
        return TranspileBlock(kind='code:escape', indentlevel=indentation.last, indentchar=indentation.symb);
    elif typ == 'quickescapeonce':
        indentation.decrOffset;
        return TranspileBlock(kind='code:escape:1', indentlevel=indentation.last, indentchar=indentation.symb);
    raise Exception('Could not parse expression!');

def parseBlockCode(u: Tree, indentation: IndentationTracker, offset: str = '') -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'blockcode':
        return parseBlockCode(children[0], indentation=indentation, offset=offset);
    if typ == 'blockcode_indent_spaces':
        return parseBlockCode(children[0], indentation=indentation, offset=offset + ' ');
    if typ == 'blockcode_indent_tabs':
        return parseBlockCode(children[0], indentation=indentation, offset=offset + '\t');
    if typ == 'blockcode_plain':
        instructions = parseInstructions(children[0]);
        block = parseBlockCode(children[1], indentation=indentation, offset=offset);
        block.parameters = dict(instructions=instructions);
        return block;
    elif typ == 'blockcode_inside':
        indentation.initOffset(offset);
        lenOffset = lengthOfWhiteSpace(offset);
        lines = [ lexedToStr(child) for child in children ];
        lenIndentation = [ lengthOfWhiteSpace(line) for line in lines ];
        assert all( n >= lenOffset + 1 for n in lenIndentation ), 'Invalid indentation inside code block!';
        lines = formatBlockUnindent(lines=lines, reference=offset + indentation.symb);
        is_under_splitline = False;
        for k, line in enumerate(lines):
            if k == 0 or not is_under_splitline:
                indentation.setOffset(line);
            if re.match(r'^.*\\$', line):
                is_under_splitline = True;
            if re.match(r'^.*:\s*$', line):
                indentation.incrOffset();
        return TranspileBlock(kind='code', content='\n'.join(lines), indentlevel=0, indentchar=indentation.symb);
    raise Exception('Could not parse expression!');

## MISCELLANEOUS PARSERS

def parseCodeInline(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'codeinline':
        return parseCodeInline(children[0], indentation=indentation);
    elif typ == 'codeoneline':
        return TranspileBlock(kind='code:inline', content=lexedToStr(u), indentlevel=indentation.last, indentchar=indentation.symb);
    elif typ == 'codemultiline':
        exprs = [ lexedToStr(child) for child in children ];
        return TranspileBlock(kind='code:inline', content='\n'.join(exprs), indentlevel=indentation.last, indentchar=indentation.symb);
    raise Exception('Could not parse expression!');

def parseInstructions(u: Tree) -> Tuple[List[str], Dict[str, Any]]:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'instructions':
        return parseArgList(children[0]);
    raise Exception('Could not parse expression!');

def parseArgList(u: Tree) -> Tuple[List[str], Dict[str, Any]]:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'arglist':
        tokens = [];
        kwargs = dict();
        for child in children:
            grandchildren = filterSubexpr(child);
            if child.data == 'argoption_token':
                value = lexedToStr(grandchildren[0]);
                tokens.append(value);
            elif child.data == 'argoption_kwarg':
                key = lexedToStr(grandchildren[0]);
                value = lexedToStr(grandchildren[1]);
                try:
                    value = json.loads(value);
                except:
                    pass;
                kwargs[key] = value;
        return tokens, kwargs;
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
