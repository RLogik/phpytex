#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from lark import Lark;
from lark import Tree;
from typing import Dict;
from typing import List;
from typing import Union;

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
        _indent_level = 0;
        return [ lexedToBlock(child, indentation=indentation) for child in children ];
    raise Exception('Could not parse expression!');

def lexedToBlock(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'newlines':
        return TranspileBlock(kind='text:linebreak', indentlevel=indentation.last, indentchar=indentation.symb);
    elif typ == 'block':
        return lexedToBlock(children[0], indentation=indentation);
    ## TEXT CONTENT
    elif type == 'blockcontent':
        expr = '';
        exprs = [];
        subst: Dict[str, TranspileBlock] = dict();
        i = 0;
        for child in children:
            if child.data == 'text':
                text = escapeForPython(lexedToStr(child));
                exprs.append(text);
            elif child.data == 'codeinline':
                key = 'subst' +  str(i);
                subblock = lexedToCodeInline(child, indentation=indentation);
                subst[key] = subblock;
                exprs.append('{{{}}}'.format(key));
                i += 1;
        block = TranspileBlock(kind='text:subst', content=expr, indentlevel=indentation.last, indentchar=indentation.symb);
        block.subst = subst;
        return block;
    ## CODE BLOCK
    elif type == 'blockcode':
        return lexedToBlockCode(children[0], indentation=indentation);
    ## QUICK COMMAND
    elif type == 'blockquick':
        return lexedToBlockQuickCommand(children[0], indentation=indentation);
    raise Exception('Could not parse expression!');

def lexedToBlockQuickCommand(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
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

def lexedToCodeInline(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'codeinline':
        return lexedToCodeInline(children[0], indentation=indentation);
    elif typ == 'codenobreaks':
        return TranspileBlock(kind='code:inline', content=lexedToStr(u), indentlevel=indentation.last, indentchar=indentation.symb);
    elif typ == 'codecontent':
        exprs = [ lexedToStr(child) for child in children ];
        return TranspileBlock(kind='code:inline', content='\n'.join(exprs), indentlevel=indentation.last, indentchar=indentation.symb);
    raise Exception('Could not parse expression!');

def lexedToBlockCode(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'blockcode':
        if len(children) == 2:
            instructions = lexedToStr(children[0]);
            indentation.initOffset('');
            block = lexedToBlockCode(children[1], indentation=indentation);
            block.parameters = dict(instructions=instructions);
            return block;
        elif len(children) == 4:
            indentOffset = lexedToStr(children[0]);
            indentOffsetEnd = lexedToStr(children[3]);
            assert indentOffset == indentOffsetEnd, 'Inconsistent indentation of code block!';
            indentation.initOffset(indentOffset);
            instructions = lexedToStr(children[1]);
            block = lexedToBlockCode(children[2], indentation=indentation);
            block.parameters = dict(instructions=instructions);
    elif typ == 'insidecode':
        ## TODO
        pass;
        # def getIndentationLevel(u: str, tab: str) -> int:
        #     n = 0;
        #     while True:
        #         if not u.startswith(tab*(n+1)):
        #             break;
        #         n += 1;
        #     return n;
        # lines = '\n'.join([ indentoffset + _indent_char + '.' ] + [ lexedToStr(child) for child in children ]);
        # lines = dedent(lines).split('\n')[1:];
        # for line in lines:
        #     _indent_level = getIndentationLevel(line, _indent_char);
        #     if re.match(r'^.*:\s*$', line):
        #         _indent_level += 1;
        # return '\n'.join(lines);
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
