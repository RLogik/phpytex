#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ..thirdparty.io import *
from ..thirdparty.misc import *
from ..thirdparty.types import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "prompt_confirmation",
    "prompt_secure_user_input",
    "prompt_user_input",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


# ----------------------------------------------------------------
# User Input
# ----------------------------------------------------------------


def prompt_user_input(message: str, expected: Callable[[str], bool]) -> Optional[str]:
    answer = None
    while True:
        try:
            answer = input(f"{message}$ ")

        # Capture Meta+C or Meta+D
        except (KeyboardInterrupt, EOFError):
            print("")
            return None

        except Exception as _:
            continue

        if expected(answer):
            break

    return answer


def prompt_secure_user_input(message: str, expected: Callable[[str], bool]) -> Optional[str]:
    answer = None
    while True:
        try:
            # TODO: show **** without line break
            answer = getpass(f"{message}$ ", stream=None)
        # Capture Meta+C or Meta+D
        except (KeyboardInterrupt, EOFError):
            print("")
            return None

        except Exception as _:
            continue

        if expected(answer):
            break
    return answer


def prompt_confirmation(message: str, default: bool = False) -> bool:
    expected = lambda x: not not re.match(
        pattern=r"^(y|yes|j|ja|n|no|nein)$",
        string=x.lower(),
        flags=re.IGNORECASE,
    )
    answer = prompt_user_input(message, expected)
    if not isinstance(answer, str):
        return default
    if re.match(pattern=r"^(y|yes|j|ja)$", string=answer.lower(), flags=re.IGNORECASE):
        return True
    return False
