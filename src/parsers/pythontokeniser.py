#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.io import *;
from src.thirdparty.types import *;
from src.thirdparty.logic import *;

from src.core.constants import *;
from src.core.log import *;
from src.core.utils import extractIndent;
from src.core.utils import sizeOfIndent;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

########
# NOTE: recursively yields the required level of indentation _after_ each lines
# E.g. lines ending in ':' command a +1 indentation level.
########
def getIndentations(codelines: list[str], indentsymb: str = '    ', encoding: str = ENCODING_UTF8) -> list[str]:
    indents = [];
    tokengroup = [];
    ## pad code lines, to allow for interrupted blocks that start off with positive indents:
    nPad = 0;
    for line in codelines:
        if not (line.strip() == ''):
            indent = extractIndent(line);
            nPad = sizeOfIndent(indent, indentsymb=indentsymb);
            codelines = [ indentsymb*i + 'pass;' for i in range(nPad) ] + codelines;
            break;
    ## cumulatively group together tokens and yield indentation:
    for token in tokenisePythonCode(code='\n'.join(codelines), encoding=encoding):
        # ignore encoding-lines, comment-lines, and empty lines (NL):
        if token.type in [ tokenize.ENCODING, tokenize.COMMENT, tokenize.NL ]:
            continue;
        # if NEWLINE or ENDMARKER reached, then end group and check indentation
        if token.type in [ tokenize.NEWLINE, tokenize.ENDMARKER ]:
            # do not record indentation for padded n blocks:
            if nPad > 0:
                nPad -= 1;
            else:
                if groupEndsInColon(tokengroup):
                    indent = getFullIndentationOfToken(tokengroup[0]);
                    indents.append(indent + indentsymb);
                else:
                    indents += getIndentationOfTokenGroup(tokengroup);
            tokengroup = [];
            continue;
        # otherwise continue to consume group:
        tokengroup.append(token);
    return indents;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def tokenisePythonCode(code: str, encoding: str = ENCODING_UTF8) -> Generator[tokenize.TokenInfo, None, None]:
    stream = io.BytesIO(code.encode('utf-8'));
    readlineObj = stream.readline;
    return tokenize.tokenize(readlineObj);

# detects if line ends in ':' (works even if line actually ends in comment or split )
def groupEndsInColon(tokengroup: list[tokenize.TokenInfo]) -> bool:
    if len(tokengroup) > 0:
        token = tokengroup[-1];
        return token.type == tokenize.OP and token.string == ':';
    return False;

def getIndentationOfTokenGroup(tokengroup: list[tokenize.TokenInfo]):
    for token in tokengroup:
        if token.type in [ tokenize.INDENT, tokenize.DEDENT ]:
            line = token.line.rstrip();
            indent = getFullIndentationOfToken(token);
            return [] if line == '' else [ indent ];
    return [];

# NOTE: tokenize does not always compute the full indentation of INDENT/DEDENT tokens, so need to manually extract
def getFullIndentationOfToken(token: tokenize.TokenInfo) -> str:
    line = token.line.rstrip();
    return extractIndent(line);
