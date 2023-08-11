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
from src.parsers.methods import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'parse_text',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHODS string -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parse_text(text: str, indentation: IndentationTracker, offset: str = '') -> Generator[TranspileBlock, None, None]:
    if text.strip() == '':
        return;
    try:
        u = tokenise_input(
            grammar_name = 'phpytex',
            grammar = GRAMMAR,
            start_token = 'blocks',
            text = text,
            collapse = True,
            prune = True,
        );
        yield from lexed_to_blocks(u, offset=offset, indentation=indentation);
    except Exception as err:
        yield from lexed_to_block_feed(text, offset=offset, indentation=indentation);
        return;
    return;

def parse_code_block(text: str, indentation: IndentationTracker, offset: str = '') -> TranspileBlock:
    u = tokenise_input('blockcode', text);
    return process_block_code(u, offset=offset, indentation=indentation);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PRIVATE METHODS: recursive lex -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# NOTE: This method is too slow. Thus only used when parse_text fails, in order to pinpoint failure.
def lexed_to_block_feed(text: str, offset: str, indentation: IndentationTracker) -> Generator[TranspileBlock, None, None]:
    lines = re.split(r'\r?\n', text);
    numlines = len(lines);
    linespos = 0;
    textrest = text;
    while not ( textrest == '' ):
        # attempt to lex next block:
        try:
            u = tokenise_input('blockfeed', textrest);
        except Exception as err:
            raise_lex_error(lines, linespos, err);
        # extract tokenised information:
        linespos_old = linespos;
        children = get_subtrees(u, remove_terminal=True);
        if len(children) > 1:
            textrest = lexed_to_string(children[1]);
            # NOTE: add character to ensure last line is not empty in line count:
            numlines_ = len(re.split(r'\r?\n', textrest + '.'));
            linespos = numlines - numlines_;
        # attempt to parse next block:
        try:
            block = lexed_to_block(children[0], offset=offset, indentation=indentation);
            yield block;
        except Exception as err:
            raise_parse_error(lines, linespos_old, linespos, err);
        # break, if not 'rest' found
        if len(children) == 1:
            break;
    return;

def lexed_to_blocks(u: LarkTree, offset: str, indentation: IndentationTracker) -> Generator[TranspileBlock, None, None]:
    typ = u.data;
    children = get_subtrees(u, remove_terminal=True);
    if typ == 'blocks':
        for child in children:
            yield lexed_to_block(child, offset=offset, indentation=indentation);
        return;
    raise Exception('Could not parse expression!');

def lexed_to_block(u: LarkTree, offset: str, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = get_subtrees(u, remove_terminal=True);
    if typ == 'blockfeedone':
        return lexed_to_block(children[0], offset=offset, indentation=indentation);
    if typ == 'block':
        return lexed_to_block(children[0], offset=offset, indentation=indentation);
    if typ == 'emptyline':
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.text,
            sub_kind = EnumTokenisationBlockSubKind.empty,
            indent_level = indentation.level,
            indent_symbol  = indentation.symbol,
        );
    # TEXT COMMENT
    elif typ == 'blockcomment':
        return lexed_to_block(children[0], offset=offset, indentation=indentation);
    elif typ == 'blockcomment_simple':
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.text,
            sub_kind = EnumTokenisationBlockSubKind.comment,
            line = lexed_to_string(u),
            indent_level = indentation.level,
            indent_symbol =indentation.symbol,
            keep = False,
        );
    elif typ == 'blockcomment_keep':
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.text,
            sub_kind = EnumTokenisationBlockSubKind.comment,
            line = lexed_to_string(u),
            indent_level = indentation.level,
            indent_symb = indentation.symbol,
            keep = True,
        );
    # TEXT CONTENT
    elif typ == 'blockcontent':
        # attempt to re-process as quick command:
        try:
            text = lexed_to_string(u);
            u = tokenise_input('blockquick', text);
            return lexed_to_quick_block(u, indentation=indentation);
        # otherwise, consider block to contain purely text + inline code:
        except:
            return process_block_content(children, indentation=indentation);
    # CODE BLOCK REGEX
    elif typ == 'blockcode_regex':
        return process_block_code_regex(lexed_to_string(u), offset=offset, indentation=indentation);
    # CODE BLOCK
    elif typ == 'blockcode':
        return process_block_code(children[0], offset=offset, indentation=indentation);
    raise Exception('Could not parse expression!');

# QUICK COMMAND
def lexed_to_quick_block(u: LarkTree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = get_subtrees(u, remove_terminal=True);
    if typ == 'blockquick':
        textindent = lexed_to_string(children[0]);
        return process_block_quick_command(children[1], textindent=textindent, indentation=indentation);
    raise Exception('Could not parse expression!');

# BLOCK PARSERS
def process_block_content(children: list[LarkTree], indentation: IndentationTracker) -> TranspileBlock:
    exprs = [];
    subst: dict[str, TokenisationBlock] = dict();
    i = 0;
    for child in children:
        if child.data == 'textcontent':
            text = escape_for_python(lexed_to_string(child), with_formatting=True);
            exprs.append(text);
        elif child.data == 'codeinline':
            key = 'subst' +  str(i);
            subblock = process_code_inline(child, indentation=indentation);
            subst[key] = subblock;
            exprs.append('{{{}}}'.format(key));
            i += 1;
    expr = ''.join(exprs);
    block = TranspileBlock(
        kind = EnumTokenisationBlockKind.text,
        sub_kind = EnumTokenisationBlockSubKind.subst,
        line = expr,
        indent_level = indentation.level,
        indent_symbol = indentation.symbol,
        substitution = subst,
    );
    return block;

def process_block_quick_command(u: LarkTree, textindent: str, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = get_subtrees(u, remove_terminal=True);
    match typ:
        case 'quickglobalset':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.set,
                indent_level = indentation.level,
                indent_symbol = indentation.symbol,
                scope = EnumTokenisationBlockScope.global_,
                variable_name = lexed_to_string(children[0]),
                variable_value = strip_end_of_code(lexed_to_string(children[1])).strip(),
            );
        case 'quicklocalset':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.set,
                indent_level = indentation.level,
                indent_symbol = indentation.symbol,
                scope = EnumTokenisationBlockScope.local,
                variable_name = lexed_to_string(children[0]),
                variable_value = strip_end_of_code(lexed_to_string(children[1])).strip(),
            );
        case 'quickinput':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.tex,
                indent_level = indentation.level,
                indent_symbol = indentation.symbol,
                path = strip_end_of_code(lexed_to_string(children[0])),
                anon = False,
                indent = textindent,
            );
        case 'quickinput_anon':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.tex,
                indent_level = indentation.level,
                indent_symbol = indentation.symbol,
                path = strip_end_of_code(lexed_to_string(children[0])),
                anon = True,
                indent = textindent,
            );
        case 'quickinput_hide':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.tex,
                indent_level = indentation.level,
                indent_symbol = indentation.symbol,
                path = strip_end_of_code(lexed_to_string(children[0])),
                anon = True,
                hide = True,
                indent = textindent,
            );
        case 'quickbib':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.bib,
                indent_level = indentation.level,
                indent_symbol = indentation.symbol,
                path = strip_end_of_code(lexed_to_string(children[0])),
                anon = False,
                indent = textindent,
            );
        case 'quickbib_anon':
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.input,
                sub_kind = EnumTokenisationBlockSubKind.bib,
                indent_level = indentation.level,
                indent_symbol = indentation.symbol,
                path = strip_end_of_code(lexed_to_string(children[0])),
                anon = True,
                indent = textindent,
            );
        case 'quickescape':
            indentation.level = 0;
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.code,
                sub_kind = EnumTokenisationBlockSubKind.escape,
                indent_level = 0,
                indent_symbol  = indentation.symbol,
            );
        case 'quickescapeonce':
            indentation -= 1; # decrease indentation by 1 level
            return TranspileBlock(
                kind = EnumTokenisationBlockKind.code,
                sub_kind = EnumTokenisationBlockSubKind.escape,
                indent_level = indentation.level,
                indent_symbol  = indentation.symbol,
            );
    raise Exception('Could not parse expression!');

# see .lark file for regex pattern
def process_block_code_regex(text: str, offset: str, indentation: IndentationTracker) -> TranspileBlock:
    text = dedent(text);
    return parse_code_block(text, offset=offset, indentation=indentation);

def process_block_code(u: LarkTree, offset: str, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = get_subtrees(u, remove_terminal=True);
    if typ == 'blockcode':
        instructions = process_block_code_arguments(children[0]);
        tokens, kwargs = instructions;
        option_import = 'import' in tokens;
        option_print = 'print' in tokens or kwargs.get('print', False);
        option_print = option_print if isinstance(option_print, bool) else False;
        block = process_block_code(children[1], offset=offset, indentation=indentation);
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
                indent_symbol = indentation.symbol,
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
        lines = [ lexed_to_string(child) for child in children ];
        lenIndentation = [
            length_of_white_space(extract_indent(line))
            for line in lines
            if not re.match(r'^\s*$', line) # ignore indentation of empty lines
        ];
        assert all( n >= lenOffset for n in lenIndentation ), 'One or more lines inside code block are too far left of acceptable minimal offset.';
        lines = text_block_unindent(lines=lines, reference=offset);
        # NOTE: uses python's tokenize module to extract syntactic information:
        final_indent = get_final_indentation(lines, indent_symbol=indentation.symbol, encoding=EnumEncoding.utf_8);
        if final_indent is not None:
            indentation.set_offset(final_indent);
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            lines = lines,
            indent_level = 0,
            indent_symbol = indentation.symbol,
        );
    raise Exception('Could not parse expression!');

# MISCELLANEOUS PARSERS

def process_code_inline(u: LarkTree, indentation: IndentationTracker) -> TranspileBlock:
    typ = u.data;
    children = get_subtrees(u, remove_terminal=True);
    indent = indentation.symbol * indentation.level;
    if typ == 'codeinline':
        return process_code_inline(children[0], indentation=indentation);
    elif typ == 'codeoneline':
        lines = format_value([ lexed_to_string(u) ], indent=indent);
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            sub_kind = EnumTokenisationBlockSubKind.value,
            lines = lines,
            indent_level = indentation.level,
            indent_symbol = indentation.symbol,
        );
    elif typ == 'codemultiline':
        lines = format_value([ lexed_to_string(child) for child in children ], indent=indent);
        return TranspileBlock(
            kind = EnumTokenisationBlockKind.code,
            sub_kind = EnumTokenisationBlockSubKind.value,
            lines = lines,
            indent_level = indentation.level,
            indent_symbol = indentation.symbol,
        );
    raise Exception('Could not parse expression!');

def process_block_code_arguments(u: LarkTree) -> tuple[list[str], dict[str, Any]]:
    typ = u.data;
    children = get_subtrees(u, remove_terminal=True);
    if typ == 'blockcode_args':
        return process_arg_list(children[0]);
    raise Exception('Could not parse expression!');

def process_arg_list(u: LarkTree) -> tuple[list[str], dict[str, Any]]:
    typ = u.data;
    children = get_subtrees(u, remove_terminal=True);
    if typ == 'arglist':
        tokens = [];
        kwargs = dict();
        for child in children:
            while isinstance(child, LarkTree) and not child.data in [ 'argoption_token', 'argoption_kwarg' ]:
                child = child.children[0];
            grandchildren = get_subtrees(child, remove_terminal=True);
            if child.data == 'argoption_kwarg':
                key = lexed_to_string(grandchildren[0]);
                value = lexed_to_string(grandchildren[1]);
                try:
                    value = json.loads(value);
                except:
                    pass;
                kwargs[key] = value;
            elif child.data == 'argoption_token':
                value = lexed_to_string(grandchildren[0]);
                tokens.append(value);
        return tokens, kwargs;
    raise Exception('Could not parse expression!');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ERROR HANDLING METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def raise_lex_error(lines: list[str], linepos: int, err: Exception):
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

def raise_parse_error(lines: list[str], linepos1: int, linepos2: int, err: Exception):
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
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def format_value(lines: list[str], indent: str) -> list[str]:
    if len(lines) == 0:
        return [];
    lines = text_block_unindent(lines, reference = indent);
    lines[-1] = strip_end_of_code(lines[-1]);
    return lines;

def strip_end_of_code(line: str) -> str:
    return re.sub(pattern=r'\s*;?\s*$',repl=r'',string=line);
