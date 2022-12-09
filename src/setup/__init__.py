#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.setup import config;
from src.setup import assets;
from src.setup.config import *;
from src.setup.assets import *;
from src.setup.cli import *;
from src.setup.methods import *;
from src.setup.yaml import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'GRAMMAR',
    'TEMPLATE_CONFIG',
    'TEMPLATE_EXAMPLE',
    'TEMPLATE_PHPYTEX_LINES_POST',
    'TEMPLATE_PHPYTEX_LINES_PRE',
    'VERSION',
    'assets',
    'config',
    'display_help',
    'display_usage',
    'get_arguments_from_cli',
    'is_open_source',
    'load_user_config',
    'set_open_source',
    'setup_yaml_reader',
];
