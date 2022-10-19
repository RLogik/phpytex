#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

def get_version() -> str:
    return read_asset(config.PATH_TO_VERSION).strip();

def get_grammar(fname: str) -> str:
    return read_asset(config.PATH_TO_GRAMMAR);

def get_template_phpytex_lines_pre() -> str:
    return read_asset(config.PATH_TO_TEMPLATE_PRE);

def get_template_phpytex_lines_post() -> str:
    return read_asset(config.PATH_TO_TEMPLATE_POST);
