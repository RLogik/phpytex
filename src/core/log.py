#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys;
import re;
import getpass;
from typing import Any;
from typing import Callable;
from typing import Union;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LOGGING_DEPTH: int = 0;
LOGGING_PREFIX: str = '';
QUIET_MODE: bool = False;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD set logging depth
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def SetLoggingState(state: str = 'out'):
    global LOGGING_DEPTH;
    global LOGGING_PREFIX;
    LOGGING_DEPTH = 1 if (state == 'in') else 0;
    LOGGING_PREFIX = '';
    if LOGGING_DEPTH > 0:
        LOGGING_PREFIX = '>'*LOGGING_DEPTH + ' ';
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Logging
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def logGeneric(tag: str, *lines: Any, force: bool = False, file = sys.stdout):
    if not force and QUIET_MODE:
        return;
    tag = '' if tag == '' else tag + ' ';
    for line in lines:
        print('{}{}{}'.format(LOGGING_PREFIX, tag, line), file=file);
    return;

def logPlain(*lines: Any, force: bool = False, file=sys.stdout):
    logGeneric('', *lines, force=force, file=file);

def logInfo(*lines: Any, force: bool = False, file=sys.stdout):
    logGeneric('[\033[94;1mINFO\033[0m]', *lines, force=force, file=file);

def logDebug(*lines: Any, force: bool = False, file=sys.stdout):
    logGeneric('[\033[96;1mDEBUG\033[0m]', *lines, force=force, file=file);

def logWarn(*lines: Any, force: bool = False, file=sys.stdout):
    logGeneric('[\033[93;1mWARNING\033[0m]', *lines, force=force, file=file);

def logError(*lines: Any, force: bool = False, file=sys.stdout):
    logGeneric('[\033[91;1mERROR\033[0m]', *lines, force=force, file=file);

def logFatal(*lines: Any, force: bool = False, file=sys.stdout):
    logGeneric('[\033[94;1mFATAL\033[0m]', *lines, force=force, file=file);
    exit(1);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# User Input
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def askUserInput(message: str, expectedformat: Callable) -> Union[str, None]:
    answer = None;
    while True:
        try:
            answer = input('{}{}'.format(LOGGING_PREFIX, message));
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

def askSecureUserInput(message: str, expectedformat: Callable) -> Union[str, None]:
    answer = None;
    while True:
        try:
            ## TODO: zeige **** ohne Zeilenumbruch an.
            answer = getpass.getpass('{}{}'.format(LOGGING_PREFIX, message), stream=None);
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
