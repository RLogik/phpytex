#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ..thirdparty.io import *
from ..thirdparty.system import *

from ..models.enums import *
from ..__paths__ import *
from . import basic

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'get_template_phpytex_lines_pre',
    'get_template_phpytex_lines_post',
    'get_grammar',
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

PATH_TO_ASSETS = 'assets'
TEMPLATE_FILE_PRE = 'template_pre'
TEMPLATE_FILE_POST = 'template_post'

# ----------------------------------------------------------------
# METHODS: get app config
# ----------------------------------------------------------------


def get_template_phpytex_lines_pre() -> str:
    return read_internal_asset(
        root=get_root_path(),
        path=os.path.join(PATH_TO_ASSETS, TEMPLATE_FILE_PRE),
        is_archived=basic.open_source(),
    )


def get_template_phpytex_lines_post() -> str:
    return read_internal_asset(
        root=get_root_path(),
        path=os.path.join(PATH_TO_ASSETS, TEMPLATE_FILE_POST),
        is_archived=basic.open_source(),
    )


def get_grammar(fname: str) -> str:
    return read_internal_asset(
        root=get_root_path(),
        path=os.path.join(PATH_TO_ASSETS, fname),
        is_archived=basic.open_source(),
    )
