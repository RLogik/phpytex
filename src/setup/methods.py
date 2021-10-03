#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from zipfile import ZipFile;

from src.local.misc import *;
from src.local.system import *;
from src.local.typing import *;

from src.core.utils import readTextFile;
from src.core.utils import ENCODING_UTF8;
from src.setup import appconfig;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_TO_VERSION: str = 'src/setup/VERSION';
PATH_TO_TEMPLATE_HELP: str = 'src/setup/templates/help';
PATH_TO_TEMPLATE_PHPYTEXLINES: str = 'src/setup/templates/phpytexlines';
PATH_TO_GRAMMARS: str = 'src/grammars';
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

def getTemplateHelp() -> str:
    return readFileContents(PATH_TO_TEMPLATE_HELP);

def getTemplatePhpytexLines() -> str:
    return readFileContents(PATH_TO_TEMPLATE_PHPYTEXLINES);

def getGrammar(fname: str) -> str:
    return readFileContents(os.path.join(PATH_TO_GRAMMARS, fname));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: extract path
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def extractPath(
    path:        str,
    root:        Any  = None,
    split:       bool = False,
    relative:    Any  = None,
    relative_to: Any  = None,
    ext:         Any  = None
) -> str:
    root = root if isinstance(root, str) else appconfig.getPathRoot();
    root = os.path.abspath(os.path.normpath(root));
    if os.path.isabs(path):
        relative = relative if isinstance(relative, bool) else False;
    else:
        relative = relative if isinstance(relative, bool) else True;
        path = os.path.join(root, path);
    path = os.path.abspath(os.path.normpath(path));

    if relative:
        root = relative_to if isinstance(relative_to, str) else appconfig.getPathRoot();
        root = os.path.abspath(os.path.normpath(root));
        path = os.path.relpath(path=path, start=root);

    if isinstance(ext, str):
        path = '{path}{ext}'.format(
            path = os.path.splitext(path)[0],
            ext = '' if ext == '' else '.' + ext,
        );

    return path;
