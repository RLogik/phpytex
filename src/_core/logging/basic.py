#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
import os
import sys
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Literal
from typing import TypeVar

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "LOG_LEVELS",
    "configure_logging",
    "log",
    "log_console",
    "log_debug_wrapped",
    "log_dev",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------

_IS_DEBUG: bool = False
T = TypeVar("T")

# ----------------------------------------------------------------
# ENUM
# ----------------------------------------------------------------

LOG_LEVELS = Literal[
    "DEBUG",
    "INFO",
    # "WARN",
    "WARNING",
    "ERROR",
    # "CRITICAL",
    "FATAL",
]


def get_log_level(level: str | int, /) -> int:
    if isinstance(level, str):
        level = logging.getLevelNamesMapping().get(level, logging.INFO)
    return level


# ----------------------------------------------------------------
# METHODS - CONFIGURATION
# ----------------------------------------------------------------


class LoggingLevelFilter(logging.Filter):
    def __init__(self, logging_level: int):
        super().__init__()
        self.logging_level = logging_level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self.logging_level


# fmt: skip
def configure_logging(
    *,
    name: str,
    level: LOG_LEVELS | int,
    # NOTE: currently unused
    path: str | None = None,
):
    global _IS_DEBUG
    level = get_log_level(level)
    _IS_DEBUG = level == logging.DEBUG
    logging.basicConfig(
        format=f"%(asctime)s $\x1b[92;1m{name}\x1b[0m [\x1b[1m%(levelname)s\x1b[0m] %(message)s",
        datefmt=r"%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger()
    logger.setLevel(level)
    return


# ----------------------------------------------------------------
# METHODS - SPECIAL
# ----------------------------------------------------------------


def log_debug_wrapped(cb: Callable[[], str], /):
    """
    This is like log_debug, with the difference that the message is wrapped
    and the method is only called if DEBUG-mode is active.
    Use this to save processing time
    """
    if not _IS_DEBUG:
        return
    message = cb()
    for text in message.split("\n"):
        logging.debug(text)


def log_console(*messages: Any):
    for text in messages:
        sys.stdout.write(f"{text}\n")
        sys.stdout.flush()


def log_dev(*messages: Any, path: str):  # pragma: no cover
    p = Path(path)
    if not p.exists():
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        p.touch(mode=0o644)

    with open(path, "a", encoding="utf-8") as fp:
        print(*messages, file=fp)


# ----------------------------------------------------------------
# METHODS - UNIVERSAL
# ----------------------------------------------------------------


def log(
    *messages: Any,
    level: LOG_LEVELS | int | None = None,
):
    level = get_log_level(level)
    match level:
        case None:
            return log_console(*messages)

        case "DEBUG":
            for text in messages:
                logging.debug(text)

        case "WARN" | "WARNING":
            for text in messages:
                logging.warning(text)

        case "ERROR":
            for text in messages:
                logging.error(text)

        case "CRITICAL" | "FATAL":
            message = "\n".join([str(text) for text in messages])
            logging.fatal(message)
            exit(1)

        # case "INFO":
        case _:
            for text in messages:
                logging.info(text)
