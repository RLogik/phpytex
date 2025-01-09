#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import traceback as tb

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "error_with_trace",
    "error_with_trace_multiline",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------


def error_with_trace_multiline(err: BaseException, /) -> list[str]:
    """
    Adds tracestack to an error and returns as list of lines.
    """
    return tb.format_exception(
        type(err),
        value=err,
        tb=err.__traceback__,
    )


def error_with_trace(err: BaseException, /) -> str:
    """
    Adds tracestack to an error and returns as single line.
    """
    lines = error_with_trace_multiline(err)
    return "\n".join(lines)
