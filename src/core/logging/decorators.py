#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...thirdparty.code import *
from ...thirdparty.types import *

from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'echo_function',
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------

PARAMS = ParamSpec('PARAMS')
RETURN = TypeVar('RETURN')
_depth = 0

# ----------------------------------------------------------------
# DECORATORS
# ----------------------------------------------------------------


def echo_function(
    tag: str | None = None,
    message: str | None = None,
    level: LOG_LEVELS | None = None,
    close: bool = True,
):
    '''
    Decorates method with an echo method.
    '''

    def dec(action: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN]:
        # prepare the message
        tag_ = tag or f'fct:{action.__name__}'
        message_ = message or tag_

        # modify function
        @wraps(action)
        def wrapped_action(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
            # perform logging
            global _depth

            message__ = message_.format(*_, **__)

            message__ = '-' * (_depth + 1) + '> ' + message__
            if close:
                log(message__ + '...', level=level)
            else:
                log(message__, level=level)

            # execute original function
            _depth += 1
            output = action(*_, **__)
            _depth = max(_depth - 1, 0)

            if close:
                log(message__ + ' completed.', level=level)

            return output

        return wrapped_action

    return dec
