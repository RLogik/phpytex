#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import re;
from zipfile import ZipFile;
from typing import Any;
from typing import Tuple;

from src.core.path import getAppPath;
from src.core.utils import readTextFile;
from src.core.utils import ENCODING_UTF8;
from src.setup import appconfig;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_TO_VERSION: str = 'src/setup/VERSION';
PATH_TO_TEMPLATE_HELP: str = 'src/setup/templates/help';
PATH_TO_TEMPLATE_PHPYTEXLINES_PRE: str = 'src/setup/templates/phpytexlines_pre';
PATH_TO_TEMPLATE_PHPYTEXLINES_POST: str = 'src/setup/templates/phpytexlines_post';
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

def readFile(path: str, encoding: str = ENCODING_UTF8) -> str:
    if _opensource:
        text = readTextFile(path, internal=True);
    else:
        with ZipFile(getAppPath(), 'r') as archive:
            text = archive.read(path).decode(encoding);
    return text;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: get app config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getVersion() -> str:
    return readFile(PATH_TO_VERSION).strip();

def getTemplateHelp() -> str:
    return readFile(PATH_TO_TEMPLATE_HELP);

def getTemplatePhpytexLines() -> Tuple[str, str]:
    return (
        readFile(PATH_TO_TEMPLATE_PHPYTEXLINES_PRE),
        readFile(PATH_TO_TEMPLATE_PHPYTEXLINES_POST),
    );

def getGrammar(fname: str) -> str:
    return readFile(os.path.join(PATH_TO_GRAMMARS, fname));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: extract file name
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def extractfilename(
    path:        str,
    root:        Any  = None,
    split:       bool = False,
    relative:    Any  = None,
    relative_to: Any  = None,
    ext:         Any  = None
) -> Tuple[str, str, str]:
    root = root if isinstance(root, str) else appconfig.getRootDir();
    root = os.path.abspath(os.path.normpath(root));
    if re.match(r'\:|^[\/\\]', path):
        relative = relative if isinstance(relative, bool) else False;
        path = os.path.abspath(os.path.normpath(path));
    else:
        relative = relative if isinstance(relative, bool) else True;
        path = os.path.join(root, path);
        path = os.path.abspath(os.path.normpath(path));

    if relative:
        root = relative_to;
        if not isinstance(root, str):
            root = appconfig.getRootDir();
        root = os.path.abspath(os.path.normpath(root));
        root_parts = re.split(r'/+', re.sub('^/+', '', root));
        path_parts = re.split(r'/+', re.sub('^/+', '', path));
        back = len(root_parts);
        while len(root_parts) > 0 and len(path_parts) > 0:
            if root_parts[0] == path_parts[0]:
                back -= 1;
                root_parts = root_parts[1:];
                path_parts = path_parts[1:];
                continue;
            break;
        path = os.path.join(*(['.'] + ['..']*back + path_parts));

    if isinstance(ext, str):
        path, _ = os.path.splitext(path);
        path = path if ext == '' else '{}.{}'.format(path, ext);

    if split:
        root, fname = os.path.split(path);
        path = os.path.normpath('/'.join([root, fname]));
    else:
        root = '';
        fname = '';

    return path, root, fname;
