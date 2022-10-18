#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.io import *;
from src.thirdparty.misc import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.core.constants import *;
from src.core.utils import readTextFile;
from src.setup import appconfig;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_TO_VERSION:       str = 'src/setup/VERSION';
PATH_TO_TEMPLATE_PRE:  str = 'src/setup/templates/template_pre';
PATH_TO_TEMPLATE_POST: str = 'src/setup/templates/template_post';
PATH_TO_GRAMMARS:      str = 'src/parsers/grammars';

_opensource: bool = True;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: set open source
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setOpenSource(value: bool = True):
    global _opensource;
    _opensource = value;
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: read file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def readFileContents(path: str, encoding: str = ENCODING_UTF8) -> str:
    if _opensource:
        text = readTextFile(os.path.join(appconfig.getPathApp(), path));
    else:
        with ZipFile(appconfig.getPathApp(), 'r') as archive:
            text = archive.read(path).decode(encoding);
    return text;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: get app config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getVersion() -> str:
    return readFileContents(PATH_TO_VERSION).strip();

def getTemplatePhpytexLinesPre() -> str:
    return readFileContents(PATH_TO_TEMPLATE_PRE);

def getTemplatePhpytexLinesPost() -> str:
    return readFileContents(PATH_TO_TEMPLATE_POST);

def getGrammar(fname: str) -> str:
    return readFileContents(os.path.join(PATH_TO_GRAMMARS, fname));
