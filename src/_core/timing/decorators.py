#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...thirdparty.code import *
from ...thirdparty.types import *
from .countdown import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "add_countdown",
    "add_countdown_async",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------

PARAMS = ParamSpec("PARAMS")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
RETURN = TypeVar("RETURN")

# ----------------------------------------------------------------
# DECORATORS
# ----------------------------------------------------------------


def add_countdown(
    duration: float,
):
    """
    Inserts a countdown class obj to a method

    @args
    - `duration` - duration of countdown in seconds
    """
    countdown = Countdown(duration=duration)

    def dec(
        method: Callable[Concatenate[Countdown, PARAMS], RETURN],
    ) -> Callable[PARAMS, Result[RETURN, BaseException]]:
        @wraps(method)
        def wrapped_action(
            *_: PARAMS.args,
            **__: PARAMS.kwargs,
        ) -> Result[RETURN, BaseException]:
            return method(countdown, *_, **__)

        return wrapped_action

    return dec


def add_countdown_async(
    duration: float,
):
    """
    Inserts a countdown class obj to an async method

    @args
    - `duration` - duration of countdown in seconds
    """
    countdown = Countdown(duration=duration)

    def dec(
        method: Callable[
            Concatenate[Countdown, PARAMS],
            Coroutine[T1, T2, RETURN],
        ],
    ) -> Callable[PARAMS, Coroutine[T1, T2, RETURN]]:
        @wraps(method)
        async def wrapped_action(
            *_: PARAMS.args,
            **__: PARAMS.kwargs,
        ):
            result = await method(countdown, *_, **__)
            return result

        return wrapped_action

    return dec
