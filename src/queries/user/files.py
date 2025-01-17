#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
import re

from ..._core.utils.basic import *
from ..._core.utils.io import *
from ...models.user import *
from ...setup import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "load_user_config",
    "locate_user_config",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------


def load_user_config(path: str) -> UserConfig:
    """
    Loades user config file from directory
    """
    assets = read_yaml(path)
    return UserConfig.model_validate(assets)


def locate_user_config() -> str:
    """
    Attempts to determine user config file in user working directory based on pattern.
    """
    pattern = re.compile(config.APPCONFIG.user_config_pattern)
    root = os.getcwd()
    for fname in os.listdir(root):
        if os.path.isfile(fname) and pattern.match(fname):
            return os.path.join(root, fname)

    raise Exception("Could not find or read any phpytex configuration files.")
