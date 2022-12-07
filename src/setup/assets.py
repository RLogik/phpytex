#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;

from src.setup import config;
from src.setup.methods import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'get_version',
    'get_grammar',
    'get_template_phpytex_lines_pre',
    'get_template_phpytex_lines_post',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: get app config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@make_lazy
def get_version() -> str:
    return read_asset(config.ASSET_PATHS.version).strip();

@make_lazy
def get_grammar(fname: str) -> str:
    return read_asset(config.ASSET_PATHS.grammar);

@make_lazy
def get_template_phpytex_lines_pre() -> str:
    return read_asset(config.ASSET_PATHS.template_pre);

@make_lazy
def get_template_phpytex_lines_post() -> str:
    return read_asset(config.ASSET_PATHS.template_post);
