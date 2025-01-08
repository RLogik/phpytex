#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ....models.transpilation import *
from ....thirdparty.lexers import *
from ..tokeniser import *
from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "process_block_quick_command",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def process_block_quick_command(
    u: Tree,
    textindent: str,
    indentation: IndentationTracker,
) -> TranspileBlock:
    t = u.data
    children = filter_subexpr(u)
    match t:
        case "quickglobalset":
            kind = "code:set"
            var_name = lexed_to_str(children[0])
            code_value = rstrip_code(lexed_to_str(children[1])).strip()
            parameters = TranspileBlockParameters(
                var_name=var_name,
                code_value=code_value,
                scope="global",
            )

        case "quicklocalset":
            kind = "code:set"
            var_name = lexed_to_str(children[0])
            code_value = rstrip_code(lexed_to_str(children[1])).strip()
            parameters = TranspileBlockParameters(
                var_name=var_name,
                code_value=code_value,
                scope="local",
            )

        case "quickinput":
            kind = "code:input"
            path = rstrip_code(lexed_to_str(children[0]))
            parameters = TranspileBlockParameters(
                path=path,
                tab=textindent,
                mode="input",
                anon=False,
            )

        case "quickinput_anon":
            kind = "code:input"
            path = rstrip_code(lexed_to_str(children[0]))
            parameters = TranspileBlockParameters(
                path=path,
                tab=textindent,
                mode="input",
                anon=True,
            )

        case "quickinput_hide":
            kind = "code:input"
            path = rstrip_code(lexed_to_str(children[0]))
            parameters = TranspileBlockParameters(
                path=path,
                tab=textindent,
                mode="input",
                anon=True,
                hide=True,
            )

        case "quickbib":
            kind = "code:input"
            path = rstrip_code(lexed_to_str(children[0]))
            parameters = TranspileBlockParameters(
                path=path,
                tab=textindent,
                mode="bib",
                anon=False,
                bib_mode="basic",
                bib_options="",
            )

        case "quickbib_anon":
            kind = "code:input"
            path = rstrip_code(lexed_to_str(children[0]))
            parameters = TranspileBlockParameters(
                path=path,
                tab=textindent,
                mode="bib",
                anon=True,
                bib_mode="basic",
                bib_options="",
            )

        case "quickbiblatex":
            kind = "code:input"
            path = rstrip_code(lexed_to_str(children[0]))
            parameters = TranspileBlockParameters(
                path=path,
                tab=textindent,
                mode="bib",
                anon=False,
                bib_mode="biblatex",
                bib_options="",
            )

        case "quickbiblatex_anon":
            kind = "code:input"
            path = rstrip_code(lexed_to_str(children[0]))
            parameters = TranspileBlockParameters(
                path=path,
                tab=textindent,
                mode="bib",
                anon=True,
                bib_mode="biblatex",
                bib_options="",
            )

        case "quickescape":
            kind = "code:escape"
            indentation.level = 0
            parameters = TranspileBlockParameters(level=0)

        case "quickescapeonce":
            kind = "code:escape"
            indentation.decrOffset()
            parameters = TranspileBlockParameters(level=indentation.level)

        case _:
            raise Exception("Could not parse expression!")

    return TranspileBlock(
        kind=kind,
        level=indentation.level,
        indentsymb=indentation.symb,
        parameters=parameters,
    )
