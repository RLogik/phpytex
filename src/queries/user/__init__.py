#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This submodule contains queries for parsing user settings.
'''

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from .calc import *
from .files import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'EXPORT_VARS',
    'load_user_config',
    'locate_user_config',
    'setting_indent_character',
    'setting_indent_character_re',
]
