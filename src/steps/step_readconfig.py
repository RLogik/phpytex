#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any;
from typing import Dict;

from src.core.utils import getFilesByPattern;
from src.setup import appconfig;
from src.setup.yaml.methods import setupYamlReader;
from src.setup.yaml.methods import readYamlFile;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step get config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step(fname: str) -> Dict[str, Any]:
    if fname == '':
        path = appconfig.getWorkingDirectory();
        filepattern = appconfig.getFilePattern();
        fname = (getFilesByPattern(path=path, filepattern=filepattern) + [''])[0];
    setupYamlReader();
    config = readYamlFile(fname);
    return config;
