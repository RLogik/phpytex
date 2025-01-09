#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from functools import wraps
from typing import Awaitable
from typing import Callable
from typing import ParamSpec
from typing import TypeVar

from ..utils.time import *
from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "echo_async_function",
    "echo_function",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------

PARAMS = ParamSpec("PARAMS")
RETURN = TypeVar("RETURN")
_depth = 0

# ----------------------------------------------------------------
# DECORATORS
# ----------------------------------------------------------------


def echo_function(
    tag: str | None = None,
    message: str | None = None,
    level: LOG_LEVELS | int | None = None,
    close: bool = True,
    depth: int | None = None,
):
    """
    Decorates a method with an logging before and after (including in the case of errors).
    """

    def dec(action: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN]:
        # prepare the message
        tag_ = tag or f"fct:{action.__name__}"
        message_ = message or tag_

        # modify function
        @wraps(action)
        def wrapped_action(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
            timer = Timer(logger=None)
            message_end, message_error = echo_beginning(_, __, timer=timer, depth=depth, close=close, message=message_, level=level)  # fmt: skip

            try:
                output = action(*_, **__)
                echo_end(timer=timer, close=close, message=message_end, level=level)  # fmt: skip
                return output

            except BaseException as err:
                echo_end(timer=timer, close=close, message=message_error, level=level)  # fmt: skip
                raise err

        return wrapped_action

    return dec


def echo_async_function(
    tag: str | None = None,
    message: str | None = None,
    level: LOG_LEVELS | int | None = None,
    close: bool = True,
    depth: int | None = None,
):
    """
    Decorates an async method with an logging before and after (including in the case of errors).
    """

    def dec(action: Callable[PARAMS, Awaitable[RETURN]]) -> Callable[PARAMS, Awaitable[RETURN]]:
        # prepare the message
        tag_ = tag or f"fct:{action.__name__}"
        message_ = message or tag_

        # modify function
        @wraps(action)
        async def wrapped_action(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
            timer = Timer(logger=None)
            message_end, message_error = echo_beginning(_, __, timer=timer, depth=depth, close=close, message=message_, level=level)  # fmt: skip

            try:
                output = await action(*_, **__)
                echo_end(timer=timer, close=close, message=message_end, level=level)  # fmt: skip
                return output

            except BaseException as err:
                echo_end(timer=timer, close=close, message=message_error, level=level)  # fmt: skip
                raise err

        return wrapped_action

    return dec


# ----------------------------------------------------------------
# AUXILIARY METHODS
# ----------------------------------------------------------------


def echo_beginning(
    posargs: tuple,
    kwargs: dict,
    /,
    *,
    timer: Timer,
    depth: int | None,
    close: bool,
    message: str,
    level: LOG_LEVELS | int | None,
) -> tuple[str, str]:
    """
    Auxiliary method to be performed at the start of an echo-decorated method.
    """
    global _depth
    if depth is not None:
        _depth = depth

    message__ = message.format(*posargs, **kwargs)

    message_start = "=" * (_depth + 1) + ">     " + message__
    message_end = message_error = ""
    if close:
        message_end = "=" * (_depth + 1) + "> [x] " + message__ + " | elapsed: {t:.2f}s"  # fmt: skip
        message_error = '=' * (_depth + 1) + '> [err] ' + message__ + " | elapsed: {t:.2f}s"  # fmt: skip

    log(message_start, level=level)
    _depth += 1
    timer.start()

    return message_end, message_error


def echo_end(
    *,
    timer: Timer,
    close: bool,
    message: str,
    level: LOG_LEVELS | int | None,
) -> tuple[str, str]:
    """
    Auxiliary method to be performed at the end of an echo-decorated method.
    """
    global _depth
    _depth = max(_depth - 1, 0)
    if close:
        log(message.format(t=timer.elapsed), level=level)
