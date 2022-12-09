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
from src.setup import config;

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
    'set_debug_mode',
    'set_plain_mode',
    'set_logging_level',
    'set_quiet_mode',
    'get_quiet_mode',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_DEBUG_MODE: bool = False;
_PLAIN_MODE: bool = True;
_QUIET_MODE: bool = False;
_CLOCK: Timer = Timer();

class LOG_LEVELS(Enum): # pragma: no cover
    DEBUG = logging.DEBUG;
    INFO  = logging.INFO;
    WARNING = logging.WARNING;

_LEVEL: LOG_LEVELS = LOG_LEVELS.INFO;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD get/set modes and timer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def set_level(level: LOG_LEVELS):
    global _LEVEL;
    _LEVEL = level;
    return;

def get_level() -> LOG_LEVELS:
    return _LEVEL;

def set_debug_mode(mode: bool):
    global _DEBUG_MODE;
    _DEBUG_MODE = mode;
    return;

def get_debug_mode() -> bool:
    return _DEBUG_MODE;

def get_quiet_mode() -> bool:
    return _QUIET_MODE;

def set_plain_mode(mode: bool):
    global _PLAIN_MODE;
    _PLAIN_MODE = mode;
    return;

def get_plain_mode() -> bool:
    return _PLAIN_MODE;

def set_quiet_mode(mode: bool):
    global _QUIET_MODE;
    _QUIET_MODE = mode;
    return;

def time_elapsed() -> timedelta:
    global _CLOCK;
    _CLOCK.stop();
    return _CLOCK.elapsed;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Logging
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def set_logging_level() -> None:
    '''
    Sets logging mode based on settings for quite/debug mode.
    '''
    if get_quiet_mode():
        set_level(LOG_LEVELS.WARNING);
    elif get_debug_mode():
        set_level(LOG_LEVELS.DEBUG);
    else:
        set_level(LOG_LEVELS.INFO);
    configure_logging(level=get_level());
    return;

def configure_logging(level: LOG_LEVELS): # pragma: no cover
    logging.basicConfig(
        format  = '%(asctime)s [\x1b[1m%(levelname)s\x1b[0m] %(message)s',
        level   = level.value,
        datefmt = r'%Y-%m-%d %H:%M:%S',
    );

@plain_formatting(factory=get_plain_mode)
def log_plain(*messages):
    print(*messages);

@plain_formatting(factory=get_plain_mode)
def log_debug(*messages: Any):
    logging.debug(*messages);

@plain_formatting(factory=get_plain_mode)
def log_info(*messages: Any):
    logging.info(*messages);

@plain_formatting(factory=get_plain_mode)
def log_warn(*messages: Any):
    logging.warning(*messages);

@plain_formatting(factory=get_plain_mode)
def log_error(*messages: Any):
    logging.error(*messages);

@plain_formatting(factory=get_plain_mode)
def log_fatal(*messages: Any):
    logging.fatal(*messages);
    exit(1);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEBUG LOGGING FOR DEVELOPMENT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def log_dev(*messages: Any): # pragma: no cover
    with open(config.PATHS.logging, 'a') as fp:
        print(*messages, file=fp);
