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
    'VERSION',
    'GRAMMAR',
    'TEMPLATE_CONFIG',
    'TEMPLATE_EXAMPLE',
    'TEMPLATE_PHPYTEX_LINES_PRE',
    'TEMPLATE_PHPYTEX_LINES_POST',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LAZY LOADED RESOURCES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@make_lazy
def get_version() -> str:
    return read_asset(config.ASSETS.version).strip();

@make_lazy
def get_grammar() -> str:
    return read_asset(config.ASSETS.grammar);

@make_lazy
def get_template_phpytex_lines_pre() -> str:
    return read_asset(config.ASSETS.template_pre);

@make_lazy
def get_template_phpytex_lines_post() -> str:
    return read_asset(config.ASSETS.template_post);

@make_lazy
def get_template_config() -> str:
    return read_asset(config.ASSETS.template_config);

@make_lazy
def get_template_example() -> str:
    return read_asset(config.ASSETS.template_example);

VERSION = get_version();
GRAMMAR = get_grammar();
TEMPLATE_CONFIG = get_template_config();
TEMPLATE_EXAMPLE = get_template_example();
TEMPLATE_PHPYTEX_LINES_PRE = get_template_phpytex_lines_pre();
TEMPLATE_PHPYTEX_LINES_POST = get_template_phpytex_lines_post();
