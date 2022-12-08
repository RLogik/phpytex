#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import src.paths;

from src.thirdparty.config import *;
from src.thirdparty.misc import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.setup import *;
from src.core.log import *;
from src.core.utils import *;
from src.models.internal import *;
from src.models.user import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ =  [
    'step_configure',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step get config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step_configure(
    file_config: Optional[str],
    options_parameters: Optional[dict] = None,
    options_compile: Optional[dict] = None,
    options_stamp: Optional[dict] = None,
) -> UserConfig:
    log_info('READ CONFIG STARTED');

    user_config = load_user_config(file_config);

    user_config.transpile = clean_up_compile_block(
        block = user_config.transpile or user_config.compile,
        options = options_compile,
    );
    user_config.compile = None;
    user_config.parameters = clean_up_parameters_block(
        block = user_config.parameters,
        options = options_parameters,
    );
    user_config.stamp = clean_up_stamp_block(
        block = user_config.stamp,
        options = options_stamp,
    );

    assert isinstance(user_config.transpile, UserCompileBlock);
    assert isinstance(user_config.transpile.options, UserCompileOptions);

    options = user_config.transpile.options;
    cleanup_config_paths(user_config=user_config, options=options);
    cleanup_config_indentation(user_config=user_config, options=options);
    cleanup_config_misc(user_config=user_config, options=options);

    log_info('READ CONFIG COMPLETE');
    return user_config;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS: config update
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def cleanup_config_paths(
    user_config: UserConfig,
    options: UserCompileOptions,
) -> None:
    config.PATHS.file_start = options.root;
    config.PATHS.file_output = options.output;
    return;

def cleanup_config_indentation(
    user_config: UserConfig,
    options: UserCompileOptions,
) -> None:
    use_tabs = options.tabs;
    n = options.spaces;
    if use_tabs:
        config.COMPILE_OPTIONS.indent_character = '\t';
        config.COMPILE_OPTIONS.indent_character_re = r'\t';
    else:
        config.COMPILE_OPTIONS.indent_character = n*' ';
        config.COMPILE_OPTIONS.indent_character_re = n*' ';
    return;

def cleanup_config_misc(
    user_config: UserConfig,
    options: UserCompileOptions,
) -> None:
    config.COMPILE_OPTIONS.seed = options.seed;
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS: cleanup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def clean_up_compile_block(
    block: Optional[UserCompileBlock | UserCompileOptions],
    options: Optional[dict]
) -> UserCompileBlock:
    '''
    Forces compile options to be defined, and potentially overrides options with cli arguments.
    '''
    if block is None:
        block = UserCompileBlock(options=options);

    if not isinstance(block, UserCompileBlock):
        block = UserCompileBlock(options=block);

    if options is not None:
        block.options = UserCompileOptions(**{
            **block.options,
            **options
        });
    return block;

def clean_up_parameters_block(
    block: Optional[UserParametersBlock],
    options: Optional[dict]
) -> UserParametersBlock:
    '''
    Forces parameters options to be defined, if options provided via cli arguments.
    '''
    if options is None:
        return;

    if block is None:
        block = UserParametersBlock(options=options);

    block.options = { **block.options, **options };

    return block;

def clean_up_stamp_block(
    block: Optional[UserStampBlock],
    options: Optional[dict]
) -> UserStampBlock:
    '''
    Forces stamp options to be defined, if options provided via cli arguments.
    '''
    if options is None:
        return;

    if block is None:
        block = UserStampBlock(options=options);
    block.options = { **block.options, **options };

    return block;
