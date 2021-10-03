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
from src.core.utils import escapeForPython;
from src.core.utils import formatBlockUnindent;
from src.core.utils import getAttribute;
from src.core.utils import lengthOfWhiteSpace;
from src.core.log import *;
from src.setup.methods import getGrammar;
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

def parseText(text: str, indentation: IndentationTracker) -> Generator[TranspileBlock, None, None]:
    if not ( text.strip() == '' ):
        u = tokeniseInput('blocks', text);
        yield from lexedToBlocks(u, indentation=indentation);
    return;

def parseCodeBlock(text: str, indentation: IndentationTracker) -> TranspileBlock:
    u = tokeniseInput('blockcode', text);
    return processBlockCode(u, indentation=indentation);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PRIVATE METHODS: recursive lex -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToBlocks(u: Tree, indentation: IndentationTracker) -> Generator[TranspileBlock, None, None]:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'blocks':
        for child in children:
            yield lexedToBlock(child, indentation=indentation);
        return;
    raise Exception('Could not parse expression!');

def lexedToBlock(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubexpr(u);
    if typ == 'block':
        return lexedToBlock(children[0], indentation=indentation);
    if typ == 'emptyline':
        return TranspileBlock(kind='text:linebreak', indentlevel=indentation.last, indentsymb=indentation.symb);
    ## TEXT COMMENT
    elif typ == 'blockcomment':
        return lexedToBlock(children[0], indentation=indentation);
    elif typ == 'blockcomment_simple':
        return TranspileBlock(kind='text:comment:simple', content=lexedToStr(u), indentlevel=indentation.last, indentsymb=indentation.symb);
    elif typ == 'blockcomment_keep':
        return TranspileBlock(kind='text:comment:keep', content=lexedToStr(u), indentlevel=indentation.last, indentsymb=indentation.symb);
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
            text = escapeForPython(lexedToStr(child), withformatting=True);
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
    if typ == 'quickglobalset':
        varname = lexedToStr(children[0]);
        codevalue = stripEndOfCode(lexedToStr(children[1]));
        block = TranspileBlock(kind='code:set:global', indentlevel=indentation.last, indentsymb=indentation.symb);
        block.parameters = dict(varname=varname, codevalue=codevalue);
        return block;
    if typ == 'quicklocalset':
        varname = lexedToStr(children[0]);
        codevalue = stripEndOfCode(lexedToStr(children[1]));
        block = TranspileBlock(kind='code:set:local', indentlevel=indentation.last, indentsymb=indentation.symb);
        block.parameters = dict(varname=varname, codevalue=codevalue);
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
        tokens, kwargs = instructions;
        block = processBlockCode(children[1], indentation=indentation, offset=offset);
        block.parameters = dict(instructions=instructions);
        if 'import' in tokens:
            block.kind = 'code:import';
            return block;
        elif 'print' in tokens or getAttribute(kwargs, 'print', expectedtype=bool, default=False):
            block.kind = 'code:value';
            blockcontainer = TranspileBlock(kind='text:subst', content='{subst0}', indentlevel=indentation.last, indentsymb=indentation.symb);
            blockcontainer.subst = { 'subst0': block };
            return blockcontainer;
        else:
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
