#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.config import *
from src.local.encoding import *;
from src.local.lexers import *;
from src.local.misc import *;
from src.local.typing import *;

from src.core.log import *;
from src.core.utils import dedentIgnoreEmptyLines;
from src.core.utils import escapeForPython;
from src.core.utils import extractIndent;
from src.core.utils import formatBlockUnindent;
from src.core.utils import getAttribute;
from src.core.utils import lengthOfWhiteSpace;
from src.setup.methods import getGrammar;
from src.customtypes.exports import *;
from src.parsers.pythontokeniser import getIndentations;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_grammar: Dict[str, str] = dict();
_lexer:   Dict[str, Lark] = dict();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS obtain lexer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getLexer(mode: str = 'blocks') -> Lark:
    global _grammar;
    global _lexer;
    if not (mode in _grammar):
        _grammar[mode] = getGrammar('phpytex.lark');
    if not (mode in _lexer):
        _lexer[mode] = Lark(
            _grammar[mode],
            start=mode,
            regex=True,
            parser='earley', # 'lalr', 'earley', 'cyk'
            priority='invert', # auto (default), none, normal, invert
        );
    return _lexer[mode];

def tokeniseInput(mode: str, text: str):
    try:
        return getLexer(mode).parse(text);
    except:
        raise Exception('Could not tokenise input as \033[1m{}\033[0m!'.format(mode));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHODS string -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parseText(text: str, indentation: IndentationTracker, offset: str = '') -> Generator[TranspileBlock, None, None]:
    if text.strip() == '':
        return;
    try:
        u = tokeniseInput('blocks', text);
        yield from lexedToBlocks(u, offset=offset, indentation=indentation);
    except Exception as err:
        yield from lexedToBlockFeed(text, offset=offset, indentation=indentation);
        return;
    return;

def parseCodeBlock(text: str, indentation: IndentationTracker, offset: str = '') -> TranspileBlock:
    u = tokeniseInput('blockcode', text);
    return processBlockCode(u, offset=offset, indentation=indentation);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PRIVATE METHODS: recursive lex -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## NOTE: This method is too slow. Thus only used when parseText fails, in order to pinpoint failure.
def lexedToBlockFeed(text: str, offset: str, indentation: IndentationTracker) -> Generator[TranspileBlock, None, None]:
    lines = re.split(r'\r?\n', text);
    numlines = len(lines);
    linespos = 0;
    textrest = text;
    while not ( textrest == '' ):
        ## attempt to lex next block:
        try:
            u = tokeniseInput('blockfeed', textrest);
        except Exception as err:
            raiseLexError(lines, linespos, err);
        ## extract tokenised information:
        linespos_old = linespos;
        children = filterSubExpr(u);
        if len(children) > 1:
            textrest = lexedToStr(children[1]);
            # NOTE: add character to ensure last line is not empty in line count:
            numlines_ = len(re.split(r'\r?\n', textrest + '.'));
            linespos = numlines - numlines_;
        ## attempt to parse next block:
        try:
            block = lexedToBlock(children[0], offset=offset, indentation=indentation);
            yield block;
        except Exception as err:
            raiseParseError(lines, linespos_old, linespos, err);
        ## break, if not 'rest' found
        if len(children) == 1:
            break;
    return;

def lexedToBlocks(u: Tree, offset: str, indentation: IndentationTracker) -> Generator[TranspileBlock, None, None]:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blocks':
        for child in children:
            yield lexedToBlock(child, offset=offset, indentation=indentation);
        return;
    raise Exception('Could not parse expression!');

def lexedToBlock(u: Tree, offset: str, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blockfeedone':
        return lexedToBlock(children[0], offset=offset, indentation=indentation);
    if typ == 'block':
        return lexedToBlock(children[0], offset=offset, indentation=indentation);
    if typ == 'emptyline':
        return TranspileBlock(kind='text:empty', level=indentation.level, indentsymb=indentation.symb);
    ## TEXT COMMENT
    elif typ == 'blockcomment':
        return lexedToBlock(children[0], offset=offset, indentation=indentation);
    elif typ == 'blockcomment_simple':
        parameters = dict(keep=False);
        return TranspileBlock(kind='text:comment', content=lexedToStr(u), level=indentation.level, indentsymb=indentation.symb, parameters=parameters);
    elif typ == 'blockcomment_keep':
        parameters = dict(keep=True);
        return TranspileBlock(kind='text:comment', content=lexedToStr(u), level=indentation.level, indentsymb=indentation.symb, parameters=parameters);
    ## TEXT CONTENT
    elif typ == 'blockcontent':
        ## attempt to re-process as quick command:
        try:
            text = lexedToStr(u);
            u = tokeniseInput('blockquick', text);
            return lexedToQuickBlock(u, indentation=indentation);
        ## otherwise, consider block to contain purely text + inline code:
        except:
            return processBlockContent(children, indentation=indentation);
    ## CODE BLOCK REGEX
    elif typ == 'blockcode_regex':
        return processBlockCodeRegex(lexedToStr(u), offset=offset, indentation=indentation);
    ## CODE BLOCK
    elif typ == 'blockcode':
        return processBlockCode(children[0], offset=offset, indentation=indentation);
    raise Exception('Could not parse expression!');

## QUICK COMMAND
def lexedToQuickBlock(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blockquick':
        textindent = lexedToStr(children[0]);
        return processBlockQuickCommand(children[1], textindent=textindent, indentation=indentation);
    raise Exception('Could not parse expression!');

## BLOCK PARSERS
def processBlockContent(children: List[Tree], indentation: IndentationTracker) -> TranspileBlock:
    exprs = [];
    subst: Dict[str, TranspileBlock] = dict();
    i = 0;
    margin = None;
    for child in children:
        if child.data == 'textcontent':
            text = escapeForPython(lexedToStr(child), withformatting=True);
            # store first left indentation:
            if margin is None:
                margin = re.sub(pattern=r'^(\s*)(.*[\r?\n]?)*', repl=r'\1', string=text);
            exprs.append(text);
        elif child.data == 'codeinline':
            key = 'subst' +  str(i);
            subblock = processCodeInline(child, indentation=indentation);
            subst[key] = subblock;
            exprs.append('{{{}}}'.format(key));
            i += 1;
    margin = margin or '';
    expr = ''.join(exprs);
    block = TranspileBlock(kind='text:subst', content=expr, level=indentation.level, indentsymb=indentation.symb, margin=margin);
    block.subst = subst;
    return block;

def processBlockQuickCommand(u: Tree, textindent: str, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    if typ in [ 'quickglobalset', 'quicklocalset' ]:
        varname = lexedToStr(children[0]);
        codevalue = stripEndOfCode(lexedToStr(children[1])).strip();
        parameters = dict(varname=varname, codevalue=codevalue);
        if typ == 'quickglobalset':
            parameters = { **parameters, **dict(scope='global') };
        elif typ == 'quicklocalset':
            parameters = { **parameters, **dict(scope='local') };
        return TranspileBlock(kind='code:set', level=indentation.level, indentsymb=indentation.symb, parameters=parameters);
    elif typ in [ 'quickinput', 'quickinput_anon', 'quickinput_hide', 'quickbib', 'quickbib_anon', 'quickbiblatex', 'quickbiblatex_anon' ]:
        path = stripEndOfCode(lexedToStr(children[0]));
        parameters = dict(path=path, tab=textindent);
        if typ == 'quickinput':
            parameters = { **parameters, **dict(mode='input', anon=False) };
        elif typ == 'quickinput_anon':
            parameters = { **parameters, **dict(mode='input', anon=True) };
        elif typ == 'quickinput_hide':
            parameters = { **parameters, **dict(mode='input', anon=True, hide=True) };
        elif typ == 'quickbib':
            parameters = { **parameters, **dict(mode='bib', anon=False, bib_mode='basic', bib_options='') };
        elif typ == 'quickbib_anon':
            parameters = { **parameters, **dict(mode='bib', anon=True, bib_mode='basic', bib_options='') };
        elif typ == 'quickbiblatex':
            parameters = { **parameters, **dict(mode='bib', anon=False, bib_mode='biblatex', bib_options='') };
        elif typ == 'quickbiblatex_anon':
            parameters = { **parameters, **dict(mode='bib', anon=True, bib_mode='biblatex', bib_options='') };
        return TranspileBlock(kind='code:input', level=indentation.level, indentsymb=indentation.symb, parameters=parameters);
    elif typ == 'quickescape':
        indentation.level = 0;
        parameters = dict(level=0);
        return TranspileBlock(kind='code:escape', level=indentation.level, indentsymb=indentation.symb, parameters=parameters);
    elif typ == 'quickescapeonce':
        indentation.decrOffset();
        parameters = dict(level=indentation.level);
        return TranspileBlock(kind='code:escape', level=indentation.level, indentsymb=indentation.symb, parameters=parameters);
    raise Exception('Could not parse expression!');

# see .lark file for regex pattern
def processBlockCodeRegex(text: str, offset: str, indentation: IndentationTracker) -> TranspileBlock:
    text = dedentIgnoreEmptyLines(text);
    return parseCodeBlock(text, offset=offset, indentation=indentation);

def processBlockCode(u: Tree, offset: str, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blockcode':
        instructions = processBlockCodeArguments(children[0]);
        tokens, kwargs = instructions;
        block = processBlockCode(children[1], offset=offset, indentation=indentation);
        if 'import' in tokens:
            block.kind = 'code:import';
            return block;
        elif 'print' in tokens or getAttribute(kwargs, 'print', expectedtype=bool, default=False):
            block.kind = 'code:value';
            margin = ''; # FIXME!
            blockcontainer = TranspileBlock(kind='text:subst', content='{subst0}', level=indentation.level, indentsymb=indentation.symb, margin=margin);
            blockcontainer.subst = { 'subst0': block };
            return blockcontainer;
        else:
            return block;
    elif typ == 'blockcode_inside':
        lenOffset = lengthOfWhiteSpace(offset);
        lines = [ lexedToStr(child) for child in children ];
        lenIndentation = [
            lengthOfWhiteSpace(extractIndent(line))
            for line in lines
            if not re.match(r'^\s*$', line) # ignore indentation of empty lines
        ];
        assert all( n >= lenOffset for n in lenIndentation ), 'One or more lines inside code block are too far left of acceptable minimal offset.';
        lines = formatBlockUnindent(lines=lines, reference=offset);
        # NOTE: uses python's tokenize module to extract syntactic information:
        indents = getIndentations(lines, indentsymb=indentation.symb, encoding=ENCODING_UTF8);
        if len(indents) > 0:
            indentation.setOffset(indents[-1]);
        return TranspileBlock(kind='code', lines=lines, level=0, indentsymb=indentation.symb);
    raise Exception('Could not parse expression!');

## MISCELLANEOUS PARSERS

def processCodeInline(u: Tree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    indent = indentation.symb*indentation.level;
    if typ == 'codeinline':
        return processCodeInline(children[0], indentation=indentation);
    elif typ == 'codeoneline':
        lines = formatValue([ lexedToStr(u) ], indent=indent);
        return TranspileBlock(kind='code:value', lines=lines, level=indentation.level, indentsymb=indentation.symb);
    elif typ == 'codemultiline':
        lines = formatValue([ lexedToStr(child) for child in children ], indent=indent);
        return TranspileBlock(kind='code:value', lines=lines, level=indentation.level, indentsymb=indentation.symb);
    raise Exception('Could not parse expression!');

def processBlockCodeArguments(u: Tree) -> Tuple[List[str], Dict[str, Any]]:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blockcode_args':
        return processArgList(children[0]);
    raise Exception('Could not parse expression!');

def processArgList(u: Tree) -> Tuple[List[str], Dict[str, Any]]:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'arglist':
        tokens = [];
        kwargs = dict();
        for child in children:
            while isinstance(child, Tree) and not child.data in [ 'argoption_token', 'argoption_kwarg' ]:
                child = child.children[0];
            grandchildren = filterSubExpr(child);
            if child.data == 'argoption_kwarg':
                key = lexedToStr(grandchildren[0]);
                value = lexedToStr(grandchildren[1]);
                try:
                    value = json.loads(value);
                except:
                    pass;
                kwargs[key] = value;
            elif child.data == 'argoption_token':
                value = lexedToStr(grandchildren[0]);
                tokens.append(value);
        return tokens, kwargs;
    raise Exception('Could not parse expression!');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ERROR HANDLING METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def raiseLexError(lines: List[str], linepos: int, err: Exception):
    text_consumed = lines[:linepos];
    text_remaining = lines[linepos:];
    # NOTE: display linepos + 1, as documents start with 1 not 0
    message = [ 'At line \033[1m{}\033[0m the text could not be \033[1mtokenised\033[0m:'.format(linepos+1) ];
    message.append('\033[1m--------------------------------\033[0m');
    message += [ '\033[2m{}\033[0m'.format(line) for line in text_consumed[-3:] ];
    message += [ '\033[91;1m{}\033[0m'.format(line) for line in text_remaining[:1] ];
    message += [ '\033[2m{}\033[0m'.format(line) for line in text_remaining[1:3] ];
    message.append('\033[1m--------------------------------\033[0m');
    message.append(str(err));
    logFatal(*message);

def raiseParseError(lines: List[str], linepos1: int, linepos2: int, err: Exception):
    text_consumed = lines[:linepos1];
    text_block = lines[linepos1:linepos2];
    text_remaining = lines[linepos2:];
    # NOTE: display linepos + 1, as documents start with 1 not 0
    message = [ 'At lines \033[1m{}\033[0m-\033[1m{}\033[0m the text could not be \033[1mparsed\033[0m:'.format(linepos1+1, linepos2+1) ];
    message.append('\033[1m--------------------------------\033[0m');
    message += [ '\033[2m{}\033[0m'.format(line) for line in text_consumed[-3:] ];
    message += [ '\033[91;1m{}\033[0m'.format(line) for line in text_block ];
    message += [ '\033[2m{}\033[0m'.format(line) for line in text_remaining[:3] ];
    message.append('\033[1m--------------------------------\033[0m');
    message.append(str(err));
    logFatal(*message);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS: filtration
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToStr(u: Union[str, Tree]) -> str:
    return u if isinstance(u, str) else ''.join([ lexedToStr(uu) for uu in u.children ]);

def filterOutTypeNoncapture(u: Tree):
    return not (u.data == 'noncapture' or re.match(r'[A-Z]', u.data));

def filterSubExpr(u: Tree) -> List[Tree]:
    return [ uu for uu in u.children if isinstance(uu, Tree) and filterOutTypeNoncapture(uu) ];

def filterOutNoncapture(u: Tree) -> List[Union[str, Tree]]:
    return [uu for uu in u.children if not isinstance(uu, Tree) or filterOutTypeNoncapture(uu) ];

def formatValue(lines: List[str], indent: str) -> List[str]:
    if len(lines) == 0:
        return [];
    lines = formatBlockUnindent(lines, reference = indent);
    lines[-1] = stripEndOfCode(lines[-1]);
    return lines;

def stripEndOfCode(u: str) -> str:
    return re.sub(r'^(.*\S|)\s*;\s*$', r'\1', u);
