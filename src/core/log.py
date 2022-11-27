#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.io import *;
from src.thirdparty.misc import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;
from src.thirdparty.log import *;

from src.core.timer import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'LOG_LEVELS',
    'configure_logging',
    'log_plain',
    'log_debug',
    'log_info',
    'log_warn',
    'log_error',
    'log_fatal',
    'log_dev',
    'set_ansi_mode',
    'set_debug_mode',
    'set_quiet_mode',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_LOGGING_DEBUG_FILE: str   = 'logs/debug.log';
_QUIET_MODE: bool = False;
_ANSI_MODE: bool = True;
_DEBUG_MODE: bool = False;
_CLOCK: Timer = Timer();

class LOG_LEVELS(Enum): # pragma: no cover
    INFO  = logging.INFO;
    DEBUG = logging.DEBUG;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD get/set quiet mode, logging depth, timer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_quiet_mode() -> bool:
    return _QUIET_MODE;

def set_quiet_mode(mode: bool):
    global _QUIET_MODE;
    _QUIET_MODE = mode;
    return;

def set_ansi_mode(mode: bool):
    global _ANSI_MODE;
    _ANSI_MODE = mode;
    return;

def get_ansi_mode() -> bool:
    return _ANSI_MODE;

def set_debug_mode(mode: bool):
    global _DEBUG_MODE;
    _DEBUG_MODE = mode;
    configure_logging(level=LOG_LEVELS.DEBUG if mode else LOG_LEVELS.INFO);
    return;

def get_debug_mode() -> bool:
    return _DEBUG_MODE;

def time_elapsed() -> timedelta:
    global _CLOCK;
    _CLOCK.stop();
    return _CLOCK.elapsed;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Logging
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def configure_logging(level: LOG_LEVELS): # pragma: no cover
    logging.basicConfig(
        format  = '%(asctime)s [\x1b[1m%(levelname)s\x1b[0m] %(message)s',
        level   = level.value,
        datefmt = r'%Y-%m-%d %H:%M:%S',
    );

@ansi_formatting(factory=get_ansi_mode)
def log_plain(*messages):
    print(*messages);

@ansi_formatting(factory=get_ansi_mode)
def log_debug(*messages: Any):
    logging.debug(*messages);

@ansi_formatting(factory=get_ansi_mode)
def log_info(*messages: Any):
    logging.info(*messages);

@ansi_formatting(factory=get_ansi_mode)
def log_warn(*messages: Any):
    logging.warning(*messages);

@ansi_formatting(factory=get_ansi_mode)
def log_error(*messages: Any):
    logging.error(*messages);

@ansi_formatting(factory=get_ansi_mode)
def log_fatal(*messages: Any):
    logging.fatal(*messages);
    exit(1);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEBUG LOGGING FOR DEVELOPMENT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def log_dev(*messages: Any): # pragma: no cover
    with open(_LOGGING_DEBUG_FILE, 'a') as fp:
        print(*messages, file=fp);
