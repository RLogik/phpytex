#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...thirdparty.misc import *
from ...thirdparty.lexers import *

from ...core.utils import *
from ...models.enums import *
from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'compute_indentations',
]

# ----------------------------------------------------------------
# MAIN METHOD
# ----------------------------------------------------------------


def compute_indentations(
    codelines: list[str],
    indentsymb: str = '    ',
    encoding: Encoding = Encoding.UTF8,
) -> list[str]:
    '''
    Use python's tokenize module to extract syntactic information.

    Recursively yields the required level of indentation _after_ each lines
    E.g. lines ending in ':' command a +1 indentation level.
    '''
    # first need to pad code to prevent parser from failing for interrupted blocks.
    pad = get_padding(codelines, indentsymb=indentsymb)
    codelines = [indentsymb * i + 'pass;' for i in range(pad)] + codelines

    # cumulatively group together tokens and yield indentation:
    indents = []
    tokengroup = []
    for token in tokenise_code(code='\n'.join(codelines), encoding=encoding):
        # ignore encoding-lines, comment-lines, and empty lines (NL):
        if token.type in [tokenize.ENCODING, tokenize.COMMENT, tokenize.NL]:
            continue

        # if NEWLINE or ENDMARKER reached, then end group and check indentation
        if token.type in [tokenize.NEWLINE, tokenize.ENDMARKER]:
            # do not record indentation for padded n blocks:
            if pad > 0:
                pad -= 1
            else:
                if group_ends_in_colon(tokengroup):
                    indent = get_full_indentation(tokengroup[0])
                    indents.append(indent + indentsymb)
                else:
                    indents += get_indentation_of_group(tokengroup)
            tokengroup = []
            continue

        # otherwise continue to consume group:
        tokengroup.append(token)

    return indents
