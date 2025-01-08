#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...._core.utils.basic import *
from ....models.enums import *
from ....models.transpilation import *
from ....thirdparty.lexers import *
from ....thirdparty.misc import *
from ... import parser_python
from ..tokeniser import *
from .basic import *
from .process_misc import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "process_block_code",
    "process_block_code_regex",
    "process_block_content",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def process_block_content(
    children: list[Tree],
    indentation: IndentationTracker,
) -> TranspileBlock:
    exprs = []
    subst: dict[str, TranspileBlock] = dict()
    index = 0
    margin = None

    for child in children:
        match child.data:
            case "textcontent":
                text = parser_python.escape_code(lexed_to_str(child), fmt=True)
                # store first left indentation:
                if margin is None:
                    margin = re.sub(pattern=r"^(\s*)(.*[\r?\n]?)*", repl=r"\1", string=text)
                exprs.append(text)

            case "codeinline":
                key = f"subst_{index}"
                subblock = process_code_inline(child, indentation=indentation)
                subst[key] = subblock
                exprs.append(f"{{{key}}}")
                index += 1

    margin = margin or ""
    expr = "".join(exprs)
    block = TranspileBlock(
        kind="text:subst",
        content=expr,
        level=indentation.level,
        indentsymb=indentation.symb,
        margin=margin,
    )
    block.subst = subst

    return block


def process_block_code(
    u: Tree,
    offset: str,
    indentation: IndentationTracker,
) -> TranspileBlock:
    children = filter_subexpr(u)
    match u.data:
        case "blockcode":
            instructions = process_block_code_arguments(children[0])
            tokens, kwargs = instructions

            try:
                option_print = kwargs.get("print", False)
                assert isinstance(option_print, bool)

            except Exception:
                option_print = False

            block = process_block_code(children[1], offset=offset, indentation=indentation)

            if "import" in tokens:
                block.kind = "code:import"
                return block

            elif "print" in tokens or option_print:
                block.kind = "code:value"
                margin = ""
                # FIXME! <- unclear what was wrong with this.
                blockcontainer = TranspileBlock(
                    kind="text:subst",
                    content="{subst0}",
                    level=indentation.level,
                    indentsymb=indentation.symb,
                    margin=margin,
                )
                blockcontainer.subst = {"subst0": block}
                return blockcontainer

            return block

        case "blockcode_inside":
            lenOffset = len_whitespace(offset)
            lines = [lexed_to_str(child) for child in children]
            lenIndentation = [
                len_whitespace(line, mode=-1)  # compute predent
                for line in lines
                if not re.match(r"^\s*$", line)  # ignore indentation of empty lines
            ]
            assert all(
                n >= lenOffset for n in lenIndentation
            ), "One or more lines inside code block are too far left of acceptable minimal offset."
            lines = unindent_lines(lines=lines, reference=offset)
            indents = parser_python.compute_indentations(
                lines,
                indentsymb=indentation.symb,
                encoding=Encoding.UTF8,
            )
            if len(indents) > 0:
                indentation.setOffset(indents[-1])

            return TranspileBlock(
                kind="code", lines=lines, level=0, indentsymb=indentation.symb
            )

    raise Exception("Could not parse expression!")


def process_block_code_regex(
    tokeniser: Tokeniser,
    text: str,
    offset: str,
    indentation: IndentationTracker,
) -> TranspileBlock:
    """
    NOTE: see .lark file for regex pattern
    """
    # TODO: possibly replace this by dedent(...)
    text = dedent_full(text)
    u = tokeniser.parse("blockcode", text)
    return process_block_code(u, offset=offset, indentation=indentation)
