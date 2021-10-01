#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.config import *;
from src.local.lexers import *;
from src.local.misc import *;
from src.local.typing import *;

from src.core.utils import extractIndent;
from src.core.utils import lengthOfWhiteSpace;
from src.core.utils import formatBlockUnindent;
from src.core.log import *;
from src.setup.methods import getGrammar;
from src.parsers.methods import escapeForPython;
from src.customtypes.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_lexer: Dict[str, Lark] = dict();

def getLexer(mode: str = 'blocks') -> Lark:
    global _lexer;
    if not (mode in _lexer):
        _lexer[mode] = Lark(
            getGrammar('phpytex.lark'),
            start=mode,
            regex=True,
            parser='earley' # 'lalr', 'earley', 'cyk'
        );
    return _lexer[mode];

def tokeniseInput(mode: str, text: str):
    try:
        return getLexer(mode).parse(text);
    except:
        raise Exception('Could not tokenise input!');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHODS string -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parseText(text: str, indentation: IndentationTracker) -> List[TranspileBlock]:
    blocks = [];
    if not ( text.strip() == '' ):
        u = tokeniseInput('blocks', text);
        blocks = lexedToBlocks(u, indentation=indentation);
    return blocks;

def parseCodeBlock(text: str, indentation: IndentationTracker) -> TranspileBlock:
    u = tokeniseInput('blockcode', text);
    return processBlockCode(u, indentation=indentation);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PRIVATE METHODS: recursive lex -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToBlocks(u: Tree, indentation: IndentationTracker) -> List[TranspileBlock]:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'blocks':
        return [ lexedToBlock(child, indentation=indentation) for child in children ];
        # ## FIXME: currently need to use this, because lexer does not reliably parse `blockcontent`.
        # blocks = [];
        # children = [ filterSubexpr(child)[0] if child.data == 'block' else child for child in children ];
        # i = 0;
        # while i < len(children):
        #     if children[i].data == 'blockcontent':
        #         ## NOTE: cf. logic in `lexedToBlock` method
        #         subchildren = [];
        #         while i < len(children):
        #             if not (children[i].data == 'blockcontent'):
        #                 break;
        #             subchildren += filterSubexpr(children[i])
        #             i += 1;
        #         block = processBlockContent(subchildren, indentation=indentation);
        #     else:
        #         block = lexedToBlock(children[i], indentation=indentation);
        #         i += 1;
        #     blocks.append(block);
        # return blocks;
    raise Exception('Could not parse expression!');

def lexedToBlock(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'block':
        return lexedToBlock(children[0], indentation=indentation);
    if typ == 'emptyline':
        return TranspileBlock(kind='text:linebreak', indentlevel=indentation.last, indentsymb=indentation.symb);
    ## TEXT CONTENT
    elif typ == 'blockcontent':
        return processBlockContent(children, indentation=indentation);
    ## CODE BLOCK REGEX
    elif typ == 'blockcode_regex':
        return processBlockCodeRegex(lexedToStr(u), indentation=indentation);
    ## CODE BLOCK
    elif typ == 'blockcode':
        return processBlockCode(children[0], indentation=indentation);
    ## QUICK COMMAND
    elif typ == 'blockquick':
        return processBlockQuickCommand(children[0], indentation=indentation);
    raise Exception('Could not parse expression!');

## BLOCK PARSERS
def processBlockContent(children: List[Tree], indentation: IndentationTracker) -> TranspileBlock:
    exprs = [];
    subst: Dict[str, TranspileBlock] = dict();
    i = 0;
    for child in children:
        if child.data == 'textcontent':
            text = escapeForPython(lexedToStr(child));
            exprs.append(text);
        elif child.data == 'codeinline':
            key = 'subst' +  str(i);
            subblock = processCodeInline(child, indentation=indentation);
            subst[key] = subblock;
            exprs.append('{{{}}}'.format(key));
            i += 1;
    expr = ''.join(exprs);
    block = TranspileBlock(kind='text:subst', content=expr, indentlevel=indentation.last, indentsymb=indentation.symb);
    block.subst = subst;
    return block;

def processBlockQuickCommand(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'quickset':
        varname = lexedToStr(children[0]);
        value = stripEndOfCode(lexedToStr(children[1]));
        block = TranspileBlock(kind='code:set', indentlevel=indentation.last, indentsymb=indentation.symb);
        block.parameters = dict(varname=varname, value=value);
        return block;
    elif typ == 'quickinput':
        path = stripEndOfCode(lexedToStr(children[0]));
        block = TranspileBlock(kind='code:input', content=path, indentlevel=indentation.last, indentsymb=indentation.symb);
        block.parameters = dict(path=path);
        return block;
    elif typ == 'quickinput_anon':
        path = stripEndOfCode(lexedToStr(children[0]));
        block = TranspileBlock(kind='code:input:anon', content=path, indentlevel=indentation.last, indentsymb=indentation.symb);
        block.parameters = dict(path=path);
        return block;
    elif typ == 'quickbib':
        path = stripEndOfCode(lexedToStr(children[0]));
        block = TranspileBlock(kind='code:bib', content=path, indentlevel=indentation.last, indentsymb=indentation.symb);
        block.parameters = dict(path=path);
        return block;
    elif typ == 'quickbib_anon':
        path = stripEndOfCode(lexedToStr(children[0]));
        block = TranspileBlock(kind='code:bib:anon', content=path, indentlevel=indentation.last, indentsymb=indentation.symb);
        block.parameters = dict(path=path);
        return block;
    elif typ == 'quickescape':
        indentation.last = 1;
        block = TranspileBlock(kind='code:escape', indentlevel=indentation.last, indentsymb=indentation.symb);
        return block;
    elif typ == 'quickescapeonce':
        indentation.decrOffset();
        block = TranspileBlock(kind='code:escape:1', indentlevel=indentation.last, indentsymb=indentation.symb);
        return block;
    raise Exception('Could not parse expression!');

# see .lark file for regex pattern
def processBlockCodeRegex(text: str, indentation: IndentationTracker) -> TranspileBlock:
    text = dedent(text);
    return parseCodeBlock(text, indentation=indentation);

def processBlockCode(u: Tree, indentation: IndentationTracker, offset: str = '') -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'blockcode':
        instructions = processInstructions(children[0]);
        block = processBlockCode(children[1], indentation=indentation, offset=offset);
        block.parameters = dict(instructions=instructions);
        return block;
    elif typ == 'blockcode_inside':
        lenOffset = lengthOfWhiteSpace(offset);
        lines = [ lexedToStr(child) for child in children ];
        lenIndentation = [ lengthOfWhiteSpace(extractIndent(line)) for line in lines ];
        assert all( n >= lenOffset for n in lenIndentation ), 'Invalid indentation inside code block!';
        lines = formatBlockUnindent(lines=lines, reference=offset + indentation.symb);
        indentation.initOffset(''); # <- NOTE: have dedented, thus offsett now empty.
        is_under_splitline = False;
        for k, line in enumerate(lines):
            indent = extractIndent(line);
            if k == 0 or not is_under_splitline:
                indentation.setOffset(indent);
            is_under_splitline = False;
            if re.match(r'^.*\\$', line):
                is_under_splitline = True;
            if re.match(r'^.*:\s*$', line):
                indentation.incrOffset();
        return TranspileBlock(kind='code', lines=lines, indentlevel=indentation.start, indentsymb=indentation.symb);
    raise Exception('Could not parse expression!');

## MISCELLANEOUS PARSERS

def processCodeInline(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    indent = indentation.symb*indentation.last;
    if typ == 'codeinline':
        return processCodeInline(children[0], indentation=indentation);
    elif typ == 'codeoneline':
        lines = formatValue([ lexedToStr(u) ], indent=indent);
        return TranspileBlock(kind='code:value', lines=lines, indentlevel=indentation.last, indentsymb=indentation.symb);
    elif typ == 'codemultiline':
        lines = formatValue([ lexedToStr(child) for child in children ], indent=indent);
        return TranspileBlock(kind='code:value', lines=lines, indentlevel=indentation.last, indentsymb=indentation.symb);
    raise Exception('Could not parse expression!');

def processInstructions(u: Tree) -> Tuple[List[str], Dict[str, Any]]:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'blockcode_instructions':
        return processArgList(children[0]);
    raise Exception('Could not parse expression!');

def processArgList(u: Tree) -> Tuple[List[str], Dict[str, Any]]:
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

def formatValue(lines: List[str], indent: str) -> List[str]:
    if len(lines) == 0:
        return [];
    lines = formatBlockUnindent(lines, reference = indent);
    lines[-1] = stripEndOfCode(lines[-1]);
    return lines;

def stripEndOfCode(u: str) -> str:
    return re.sub(r'^(.*\S|)\s*;\s*$', r'\1', u);
