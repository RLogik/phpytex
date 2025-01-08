#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...thirdparty.config import *
from ...thirdparty.types import *
from ...thirdparty.misc import *
from ...thirdparty.system import *

from ..._core.utils.basic import *
from ...models.user import *
from ...setup import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'locate_user_config',
    'load_user_config',
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------


def load_user_config(path: str) -> UserConfig:
    '''
    Loades user config file from directory
    '''
    with open(path, 'r') as fp:
        assets = yaml.load(fp, Loader=yaml.FullLoader)
        return UserConfig.model_validate(assets)


def locate_user_config() -> str:
    '''
    Attempts to determine user config file in user working directory based on pattern.
    '''
    pattern = re.compile(config.APPCONFIG.user_config_pattern)
    root = os.getcwd()
    for fname in os.listdir(root):
        if os.path.isfile(fname) and pattern.match(fname):
            return os.path.join(root, fname)
    raise Exception('Could not find or read any phpytex configuration files.')
