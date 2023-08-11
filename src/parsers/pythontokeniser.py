#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.io import *;
from src.thirdparty.types import *;
from src.thirdparty.logic import *;

from src.models.internal import *;
from src.core.constants import *;
from src.core.log import *;
from src.core.utils import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'get_final_indentation',
    'get_indentations',
    'tokenise_python_code',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_final_indentation(
    lines: list[str],
    indent_symbol: str = '    ',
    encoding: EnumEncoding = EnumEncoding.utf_8,
) -> Optional[str]:
    '''
    Yields the final required level of indentation _after_ each final line.
    '''
    indent = None;
    for _indent in get_indentations(lines=lines, indent_symbol=indent_symbol, encoding=encoding):
        indent = _indent;
    return indent;

def get_indentations(
    lines: list[str],
    indent_symbol: str = '    ',
    encoding: EnumEncoding = EnumEncoding.utf_8,
) -> Generator[str, None, None]:
    '''
    Recursively yields the required level of indentation _after_ each lines
    E.g. lines ending in ':' receive a +1 indentation level.
    '''
    tokengroup = [];
    # pad code lines, to allow for interrupted blocks that start off with positive indents:
    nPad = 0;
    for line in lines:
        if not (line.strip() == ''):
            indent = extract_indent(line);
            nPad, _ = size_of_indent(indent, indent_symbol=indent_symbol);
            lines = [ f'{indent_symbol * i}pass;' for i in range(nPad) ] + lines;
            break;
    # cumulatively group together tokens and yield indentation:
    for token in tokenise_python_code(code='\n'.join(lines), encoding=encoding):
        match token.type:
            # ignore encoding-lines, comment-lines, and empty lines (NL):
            case tokenize.ENCODING | tokenize.COMMENT | tokenize.NL:
                pass;
            # if NEWLINE or ENDMARKER reached, then end group and check indentation
            case tokenize.NEWLINE | tokenize.ENDMARKER:
                # do not record indentation for padded n blocks:
                if nPad > 0:
                    nPad -= 1;
                elif group_ends_in_colon(tokengroup):
                    indent = get_full_indentation_of_token(tokengroup[0]);
                    yield indent + indent_symbol;
                else:
                    yield from get_indentation_of_token_group;
                tokengroup = [];
            # otherwise continue to consume group:
            case _:
                tokengroup.append(token);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def tokenise_python_code(code: str, encoding: EnumEncoding) -> Generator[tokenize.TokenInfo, None, None]:
    '''
    Uses native python module 'tokenize' to tokenise a string.
    '''
    stream = io.BytesIO(code.encode(encoding.value));
    readlineObj = stream.readline;
    return tokenize.tokenize(readlineObj);

def group_ends_in_colon(tokengroup: list[tokenize.TokenInfo]) -> bool:
    '''
    Detects if line ends in ':' (works even if line actually ends in comment or split )
    '''
    if len(tokengroup) > 0:
        token = tokengroup[-1];
        return token.type == tokenize.OP and token.string == ':';
    return False;

def get_indentation_of_token_group(tokengroup: list[tokenize.TokenInfo]) -> Generator[str, None, None]:
    '''
    Extracts the first indent/dedent of a group of tokens.
    '''
    for token in tokengroup:
        if token.type in [ tokenize.INDENT, tokenize.DEDENT ]:
            line = token.line.rstrip();
            indent = get_full_indentation_of_token(token);
            if line != '':
                yield indent;
            return;
    return;

def get_full_indentation_of_token(token: tokenize.TokenInfo) -> str:
    '''
    NOTE: 'tokenize' does not always compute the full indentation of INDENT/DEDENT tokens, so need to manually extract
    '''
    line = token.line.rstrip();
    return extract_indent(line);
