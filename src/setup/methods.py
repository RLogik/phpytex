#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.__path__ import PATH_APP_INTERNAL
from zipfile import ZipFile;

from src.core.utils import readTextFile;
from src.core.utils import ENCODING_UTF8;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_TO_VERSION: str = 'src/setup/VERSION';
OPEN_SOURCE: bool = True;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setOpenSource(value: bool = True):
    global OPEN_SOURCE;
    OPEN_SOURCE = value;
    return;

def getVersion() -> str:
    version = readFile(PATH_TO_VERSION).strip();
    return version;

def readFile(path: str, encoding: str = ENCODING_UTF8) -> str:
    if OPEN_SOURCE:
        text = readTextFile(PATH_TO_VERSION, internal=True);
    else:
        with ZipFile(PATH_APP_INTERNAL, 'r') as archive:
            text = archive.read('src/setup/VERSION').decode(encoding);
    return text;
