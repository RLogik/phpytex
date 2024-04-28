#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

from ...thirdparty.log import *
from ...thirdparty.types import *
from ...thirdparty.system import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'LOG_LEVELS',
    'configure_logging',
    'log',
    'log_console',
    'log_debug',
    'log_debug_wrapped',
    'log_dev',
    'log_error',
    'log_fatal',
    'log_info',
    'log_warn',
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------

_IS_DEBUG: bool = False
_LOGGING_DEBUG_FILE: str = 'logs/debug.log'
T = TypeVar('T')

# ----------------------------------------------------------------
# ENUM
# ----------------------------------------------------------------


class LOG_LEVELS(Enum):  # pragma: no cover
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARN = logging.WARN
    ERROR = logging.ERROR
    FATAL = logging.FATAL


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
    name: str,
    level: str | LOG_LEVELS,
    path: str | None,
):
    global _IS_DEBUG
    level_ = level.value if isinstance(level, LOG_LEVELS) else level
    _IS_DEBUG = level_ == 'DEBUG'
    logging.basicConfig(
        format=f'%(asctime)s $\x1b[92;1m{name}\x1b[0m [\x1b[1m%(levelname)s\x1b[0m] %(message)s',
        datefmt=r'%Y-%m-%d %H:%M:%S',
    )
    logger = logging.getLogger()
    logger.setLevel(level_)

    formatter = logging.Formatter(
        fmt=f'%(asctime)s ${name} [%(levelname)s] %(message)s',
        datefmt=r'%Y-%m-%d %H:%M:%S',
    )
    if path is None:
        return
    for path_, filt in [
        (f'{path}/out.log', logging.INFO),
        (f'{path}/out.log', logging.WARN),
        (f'{path}/err.log', logging.ERROR),
        (f'{path}/err.log', logging.CRITICAL),
        (f'{path}/err.log', logging.FATAL),
        (f'{path}/debug.log', logging.DEBUG),
    ]:
        create_file_if_not_exists(path_)
        handler = logging.FileHandler(path_)
        handler.setLevel(filt)
        handler.setFormatter(formatter)
        handler.addFilter(LoggingLevelFilter(filt))
        logger.addHandler(handler)
    return


# ----------------------------------------------------------------
# METHODS - BASIC
# ----------------------------------------------------------------


def log_debug(*messages: Any):
    for text in messages:
        logging.debug(text)


def log_debug_wrapped(cb: Callable[[], str]):
    '''
    This is like log_debug, with the difference that the message is wrapped
    and the method is only called if DEBUG-mode is active.
    Use this to save processing time
    '''
    if not _IS_DEBUG:
        return
    message = cb()
    log_debug(*(message.split('\n')))


def log_console(*messages: Any):
    for text in messages:
        sys.stdout.write(f'{text}\n')
        sys.stdout.flush()


def log_info(*messages: Any):
    for text in messages:
        logging.info(text)


def log_warn(*messages: Any):
    for text in messages:
        logging.warning(text)


def log_error(*messages: Any):
    for text in messages:
        logging.error(text)


def log_fatal(*messages: Any):
    logging.fatal('\n'.join([str(text) for text in messages]))
    exit(1)


def log(*messages: Any, level: LOG_LEVELS | None):
    match level:
        case None:
            return log_console(*messages)
        case LOG_LEVELS.DEBUG:
            return log_debug(*messages)
        case LOG_LEVELS.WARN:
            return log_warn(*messages)
        case LOG_LEVELS.ERROR:
            return log_error(*messages)
        case LOG_LEVELS.FATAL:
            return log_fatal(*messages)
        # case LOG_LEVELS.INFO:
        case _:
            return log_info(*messages)


# ----------------------------------------------------------------
# DEBUG LOGGING FOR DEVELOPMENT
# ----------------------------------------------------------------


def log_dev(*messages: Any):  # pragma: no cover
    path = _LOGGING_DEBUG_FILE
    p = Path(path)
    if not p.exists():
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        p.touch(mode=0o644)
    with open(_LOGGING_DEBUG_FILE, 'a') as fp:
        print(*messages, file=fp)
