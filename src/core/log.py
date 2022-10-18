#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.io import *;
from src.thirdparty.misc import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.core.timer import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_logging_depth:  int   = 0;
_logging_prefix: str   = '';
_quietmode:      bool  = False;
_tm:             Timer = Timer();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD get/set quiet mode, logging depth, timer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getQuietMode() -> bool:
    return _quietmode;

def setQuietMode(mode: bool):
    global _quietmode;
    _quietmode = mode;
    return;

def restartTimer():
    global _tm;
    _tm.reset();
    return;

def timeElapsed() -> timedelta:
    global _tm;
    _tm.stop();
    return _tm.elapsed;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Logging
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def logGeneric(tag: str, *lines: Any, file: io.TextIOWrapper, force: bool = False, tag_all: bool = True):
    if not force and _quietmode:
        return;
    tag = '' if tag == '' else tag + ' ';
    file = file or sys.stdout;
    for line in lines:
        print('{}{}{}'.format(_logging_prefix, tag, line), file=file);
        if not tag_all:
            tag = '';
    return;

def logPlain(*lines: Any, force: bool = False, file: Any = None):
    logGeneric('', *lines, force=force, file=file or sys.stdout);

def logInfo(*lines: Any, force: bool = False, tag_all: bool = True, file: Any = None):
    logGeneric('[\033[94;1mINFO\033[0m]', *lines, force=force, tag_all=tag_all, file=file or sys.stdout);

def logDebug(*lines: Any, force: bool = False, tag_all: bool = True, file: Any = None):
    logGeneric('[\033[96;1mDEBUG\033[0m]', *lines, force=force, tag_all=tag_all, file=file or sys.stdout);

def logWarn(*lines: Any, force: bool = False, tag_all: bool = False, file: Any = None):
    logGeneric('[\033[93;1mWARNING\033[0m]', *lines, force=force, tag_all=tag_all, file=file or sys.stdout);

def logError(*lines: Any, force: bool = False, tag_all: bool = False, file: Any = None):
    logGeneric('[\033[91;1mERROR\033[0m]', *lines, force=force, tag_all=tag_all, file=file or sys.stderr);

def logFatal(*lines: Any, force: bool = False, tag_all: bool = False, file: Any = None):
    logGeneric('[\033[91;1mFATAL\033[0m]', *lines, force=force, tag_all=tag_all, file=file or sys.stderr);
    exit(1);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# User Input
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def askUserInput(message: str, expectedformat: Callable) -> Optional[str]:
    answer = None;
    while True:
        try:
            answer = input('{}{}'.format(_logging_prefix, message));
        ## Capture Meta+C:
        except KeyboardInterrupt:
            logPlain('');
            return None;
        ## Capture Meta+D:
        except EOFError:
            logPlain('');
            return None;
        except:
            continue;
        if expectedformat(answer):
            break;
    return answer;

def askSecureUserInput(message: str, expectedformat: Callable) -> Optional[str]:
    answer = None;
    while True:
        try:
            ## TODO: zeige **** ohne Zeilenumbruch an.
            answer = getpass('{}{}'.format(_logging_prefix, message), stream=None);
        ## Capture Meta+C:
        except KeyboardInterrupt:
            logPlain('');
            return None;
        ## Capture Meta+D:
        except EOFError:
            logPlain('');
            return None;
        except:
            continue;
        if expectedformat(answer):
            break;
    return answer;

def askConfirmation(message: str, default: bool = False) -> bool:
    answer = askUserInput(message, lambda x: not not re.match(r'^(y|yes|j|ja|n|no|nein)$', x));
    if isinstance(answer, str):
        return True if re.match(r'^(y|yes|j|ja)$', answer) else False;
    return default;
