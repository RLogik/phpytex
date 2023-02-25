#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.config import *
from src.thirdparty.logic import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.setup import *;
from src.core.constants import *;
from src.core.log import *;
from src.core.utils import *;
from src.models.internal import *;
from src.parsers import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'getLexer',
    'tokeniseInput',
    'parseText',
    'parseCodeBlock',
    'lexedToBlockFeed',
    'lexedToBlocks',
    'lexedToBlock',
    'lexedToQuickBlock',
    'processBlockContent',
    'processBlockQuickCommand',
    'processBlockCodeRegex',
    'processBlockCode',
    'processCodeInline',
    'processBlockCodeArguments',
    'processArgList',
    'raiseLexError',
    'raiseParseError',
    'lexedToStr',
    'filterOutTypeNoncapture',
    'filterSubExpr',
    'filterOutNoncapture',
    'formatValue',
    'stripEndOfCode',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_grammar: dict[str, str] = dict();
_lexer:   dict[str, Lark] = dict();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS obtain lexer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getLexer(mode: str = 'blocks') -> Lark:
    global _grammar;
    global _lexer;
    if not (mode in _grammar):
        _grammar[mode] = GRAMMAR;
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

def lexedToBlocks(u: LarkTree, offset: str, indentation: IndentationTracker) -> Generator[TranspileBlock, None, None]:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blocks':
        for child in children:
            yield lexedToBlock(child, offset=offset, indentation=indentation);
        return;
    raise Exception('Could not parse expression!');

def lexedToBlock(u: LarkTree, offset: str, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blockfeedone':
        return lexedToBlock(children[0], offset=offset, indentation=indentation);
    if typ == 'block':
        return lexedToBlock(children[0], offset=offset, indentation=indentation);
    if typ == 'emptyline':
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.text,
            sub_kind = EnumTokenisationBlockSubKind.empty,
            indent_level = indentation.level,
            indent_symbol  = indentation.symb,
        );
    ## TEXT COMMENT
    elif typ == 'blockcomment':
        return lexedToBlock(children[0], offset=offset, indentation=indentation);
    elif typ == 'blockcomment_simple':
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.text,
            sub_kind = EnumTokenisationBlockSubKind.comment,
            line = lexedToStr(u),
            indent_level = indentation.level,
            indent_symbol =indentation.symb,
            keep = False,
        );
    elif typ == 'blockcomment_keep':
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.text,
            sub_kind = EnumTokenisationBlockSubKind.comment,
            line = lexedToStr(u),
            indent_level = indentation.level,
            indent_symb = indentation.symb,
            keep = True,
        );
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
def lexedToQuickBlock(u: LarkTree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blockquick':
        textindent = lexedToStr(children[0]);
        return processBlockQuickCommand(children[1], textindent=textindent, indentation=indentation);
    raise Exception('Could not parse expression!');

## BLOCK PARSERS
def processBlockContent(children: list[LarkTree], indentation: IndentationTracker) -> TranspileBlock:
    exprs = [];
    subst: dict[str, TokenisationBlock] = dict();
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
    block = TranspileBlock(
        kind = EnumTokenisationBlockKind.text,
        sub_kind = EnumTokenisationBlockSubKind.subst,
        line = expr,
        indent_level = indentation.level,
        indent_symbol = indentation.symb,
        substitution = subst,
    );
    return block;

def processBlockQuickCommand(u: LarkTree, textindent: str, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    match typ:
        case 'quickglobalset':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.set,
                indent_level = indentation.level,
                indent_symbol = indentation.symb,
                scope = EnumTokenisationBlockScope.global_,
                variable_name = lexedToStr(children[0]),
                variable_value = stripEndOfCode(lexedToStr(children[1])).strip(),
            );
        case 'quicklocalset':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.set,
                indent_level = indentation.level,
                indent_symbol = indentation.symb,
                scope = EnumTokenisationBlockScope.local,
                variable_name = lexedToStr(children[0]),
                variable_value = stripEndOfCode(lexedToStr(children[1])).strip(),
            );
        case 'quickinput':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.tex,
                indent_level = indentation.level,
                indent_symbol = indentation.symb,
                path = stripEndOfCode(lexedToStr(children[0])),
                anon = False,
                indent = textindent,
            );
        case 'quickinput_anon':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.tex,
                indent_level = indentation.level,
                indent_symbol = indentation.symb,
                path = stripEndOfCode(lexedToStr(children[0])),
                anon = True,
                indent = textindent,
            );
        case 'quickinput_hide':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.tex,
                indent_level = indentation.level,
                indent_symbol = indentation.symb,
                path = stripEndOfCode(lexedToStr(children[0])),
                anon = True,
                hide = True
                indent = textindent,
            );
        case 'quickbib':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.bib,
                indent_level = indentation.level,
                indent_symbol = indentation.symb,
                path = stripEndOfCode(lexedToStr(children[0])),
                anon = False,
                indent = textindent,
            );
        case 'quickbib_anon':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.bib,
                indent_level = indentation.level,
                indent_symbol = indentation.symb,
                path = stripEndOfCode(lexedToStr(children[0])),
                anon = True,
                indent = textindent,
            );
        case 'quickescape':
            indentation.level = 0;
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.code,
                sub_kind = EnumTokenisationBlockSubKind.escape,
                indent_level = 0,
                indent_symbol  = indentation.symb,
            );
        case 'quickescapeonce':
            indentation.decrOffset();
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.code,
                sub_kind = EnumTokenisationBlockSubKind.escape,
                indent_level = indentation.level,
                indent_symbol  = indentation.symb,
            );
    raise Exception('Could not parse expression!');

# see .lark file for regex pattern
def processBlockCodeRegex(text: str, offset: str, indentation: IndentationTracker) -> TranspileBlock:
    text = dedentIgnoreEmptyLines(text);
    return parseCodeBlock(text, offset=offset, indentation=indentation);

def processBlockCode(u: LarkTree, offset: str, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blockcode':
        instructions = processBlockCodeArguments(children[0]);
        tokens, kwargs = instructions;
        option_import = 'import' in tokens;
        option_print = 'print' in tokens or kwargs.get('print', False);
        option_print = option_print if isinstance(option_print, bool) else False;
        block = processBlockCode(children[1], offset=offset, indentation=indentation);
        if option_import:
            block.kind = EnumTokenisationBlockKind.code;
            block.sub_kind = EnumTokenisationBlockSubKind.import_;
            return block;
        elif option_print:
            block.kind = EnumTokenisationBlockKind.code;
            block.sub_kind = EnumTokenisationBlockSubKind.value;
            blockcontainer = TranspileBlock(
                kind = EnumTokenisationBlockKind.text,
                sub_kind = EnumTokenisationBlockSubKind.subst,
                indent_level = indentation.level,
                indent_symbol = indentation.symb,
                line = r'{subst0}',
                substitution = {
                    'subst0': block,
                },
            );
            return blockcontainer;
        else:
            return block;
    elif typ == 'blockcode_inside':
        lenOffset = length_of_white_space(offset);
        lines = [ lexedToStr(child) for child in children ];
        lenIndentation = [
            length_of_white_space(extractIndent(line))
            for line in lines
            if not re.match(r'^\s*$', line) # ignore indentation of empty lines
        ];
        assert all( n >= lenOffset for n in lenIndentation ), 'One or more lines inside code block are too far left of acceptable minimal offset.';
        lines = formatBlockUnindent(lines=lines, reference=offset);
        # NOTE: uses python's tokenize module to extract syntactic information:
        indents = getIndentations(lines, indentsymb=indentation.symb, encoding=ENCODING_UTF8);
        if len(indents) > 0:
            indentation.setOffset(indents[-1]);
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            lines = lines,
            indent_level = 0,
            indent_symbol = indentation.symb,
        );
    raise Exception('Could not parse expression!');

## MISCELLANEOUS PARSERS

def processCodeInline(u: LarkTree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = filterSubExpr(u);
    indent = indentation.symb*indentation.level;
    if typ == 'codeinline':
        return processCodeInline(children[0], indentation=indentation);
    elif typ == 'codeoneline':
        lines = formatValue([ lexedToStr(u) ], indent=indent);
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            sub_kind = EnumTokenisationBlockSubKind.value,
            lines = lines,
            indent_level = indentation.level,
            indent_symbol = indentation.symb,
        );
    elif typ == 'codemultiline':
        lines = formatValue([ lexedToStr(child) for child in children ], indent=indent);
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            sub_kind = EnumTokenisationBlockSubKind.value,
            lines = lines,
            indent_level = indentation.level,
            indent_symbol = indentation.symb,
        );
    raise Exception('Could not parse expression!');

def processBlockCodeArguments(u: LarkTree) -> tuple[list[str], dict[str, Any]]:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'blockcode_args':
        return processArgList(children[0]);
    raise Exception('Could not parse expression!');

def processArgList(u: LarkTree) -> tuple[list[str], dict[str, Any]]:
    typ = u.data;
    children = filterSubExpr(u);
    if typ == 'arglist':
        tokens = [];
        kwargs = dict();
        for child in children:
            while isinstance(child, LarkTree) and not child.data in [ 'argoption_token', 'argoption_kwarg' ]:
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

def raiseLexError(lines: list[str], linepos: int, err: Exception):
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
    log_fatal(*message);

def raiseParseError(lines: list[str], linepos1: int, linepos2: int, err: Exception):
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
    log_fatal(*message);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS: filtration
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToStr(u: str | LarkTree) -> str:
    return u if isinstance(u, str) else ''.join([ lexedToStr(uu) for uu in u.children ]);

def filterOutTypeNoncapture(u: LarkTree):
    return not (u.data == 'noncapture' or re.match(r'[A-Z]', u.data));

def filterSubExpr(u: LarkTree) -> list[LarkTree]:
    return [ uu for uu in u.children if isinstance(uu, LarkTree) and filterOutTypeNoncapture(uu) ];

def filterOutNoncapture(u: LarkTree) -> list[str | LarkTree]:
    return [uu for uu in u.children if not isinstance(uu, LarkTree) or filterOutTypeNoncapture(uu) ];

def formatValue(lines: list[str], indent: str) -> list[str]:
    if len(lines) == 0:
        return [];
    lines = formatBlockUnindent(lines, reference = indent);
    lines[-1] = stripEndOfCode(lines[-1]);
    return lines;

def stripEndOfCode(u: str) -> str:
    return re.sub(r'^(.*\S|)\s*;\s*$', r'\1', u);
