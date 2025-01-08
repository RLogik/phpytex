#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...models.transpilation import *
from ...thirdparty.config import *
from ...thirdparty.maths import *
from ...thirdparty.misc import *
from ...thirdparty.types import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "escape_code",
    "unparse",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def unparse(
    value: Any,
    indent: int = 0,
    multiline: bool = False,
    indentchar: str = "    ",
) -> str:
    """
    Returns an encoded version of value for implementation in python code.
    """
    conv = lambda x: unparse(x, indent=indent + 1, multiline=multiline, indentchar=indentchar)

    if isinstance(value, bool):
        # DEV-NOTE: booleans are also of type integer! Thus need to do this first.
        return str(value)

    elif isinstance(value, (str, int, float)):
        return json.dumps(value)

    elif isinstance(value, EvalType) or value is None:
        return str(value)

    elif isinstance(value, Fraction):
        return f"Fraction('{value}')"

    elif isinstance(value, tuple):
        values = list(map(conv, value))
        return unparse_iterable(values, ('(', ')'), multiline=multiline, indent=indent, indentchar=indentchar)  # fmt: skip

    elif isinstance(value, list):
        values = list(map(conv, value))
        return unparse_iterable(values, ('[', ']'), multiline=multiline, indent=indent, indentchar=indentchar)  # fmt: skip

    elif isinstance(value, dict):
        values = [f'"{key}": {conv(value)}' for key, value in value.items()]
        return unparse_iterable(values, ('{', '}'), multiline=multiline, indent=indent, indentchar=indentchar)  # fmt: skip

    raise Exception("Could not evaluated value as string")


def escape_code(text: str, fmt: bool = False) -> str:
    """
    escapes string for use in python code
    """
    text = re.sub(r"(\\+)", r"\1\1", text)
    text = re.sub(r"\n", r"\\n", text)
    text = re.sub(r"\t", r"\\t", text)
    text = re.sub(r"\"", r"\\u0022", text)
    text = re.sub(r"\'", r"\\u0027", text)
    # text = re.sub(r'\%', slash+'u0025', text);
    if fmt:
        text = re.sub(r"(\{+)", r"\1\1", text)
        text = re.sub(r"(\}+)", r"\1\1", text)
    return text


# ----------------------------------------------------------------
# AUXILIARY METHODS
# ----------------------------------------------------------------


def unparse_iterable(
    values: Iterable[str],
    braces: tuple[str, str],
    multiline: bool,
    indent: int,
    indentchar: str,
):
    sepFirst, sep, sepFinal = "", ",", ","
    if multiline and len(values) > 1:
        tab = indentchar * indent
        sepFirst = f"\n{tab + indent}"
        sep = f",\n{tab + indent}"
        sepFinal = f",\n{tab}"

    # NOTE: trailing comma is allowed for all, but necessary for tuple-type!
    contents = sep.join(values)
    if len(values) > 0:
        contents += sepFinal

    return f"{braces[0]}{sepFirst}{contents}{braces[1]}"
