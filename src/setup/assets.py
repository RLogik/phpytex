#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os

from ..__paths__ import *
from .._core.utils.io import *
from ..models.enums import *
from . import config

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "get_grammar",
    "get_grammar_transpiler",
    "get_template_phpytex_lines_post",
    "get_template_phpytex_lines_pre",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

PATH_TO_ASSETS = "assets"
TEMPLATE_FILE_PRE = "template_pre"
TEMPLATE_FILE_POST = "template_post"
GRAMMAR_TRANSPILER = "phpytex.lark"

# ----------------------------------------------------------------
# METHODS: get app config
# ----------------------------------------------------------------


def get_template_phpytex_lines_pre() -> str:
    return read_internal_asset(
        root=get_root_path(),
        path=os.path.join(PATH_TO_ASSETS, TEMPLATE_FILE_PRE),
        is_archived=config.open_source(),
    ).decode()


def get_template_phpytex_lines_post() -> str:
    return read_internal_asset(
        root=get_root_path(),
        path=os.path.join(PATH_TO_ASSETS, TEMPLATE_FILE_POST),
        is_archived=config.open_source(),
    ).decode()


def get_grammar(name: str, /) -> str:
    return read_internal_asset(
        root=get_root_path(),
        path=os.path.join(PATH_TO_ASSETS, name),
        is_archived=config.open_source(),
    ).decode()


def get_grammar_transpiler() -> str:
    return get_grammar(GRAMMAR_TRANSPILER)
