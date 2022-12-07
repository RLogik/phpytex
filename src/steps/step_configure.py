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

    # cleanup - compile options must be defined!
    if user_config.compile is None:
        user_config.compile = UserCompileBlock(options=options_compile);
    if not isinstance(user_config.compile, UserCompileBlock):
        user_config.compile = UserCompileBlock(options=user_config.compile);

    # overwrite user config with user cli args:
    if options_parameters is not None:
        if user_config.parameters is None:
            user_config.parameters = UserParameterBlock(options=options_parameters);
        user_config.parameters.options = {
            **user_config.parameters.options,
            **options_parameters
        };

    # overwrite user config with user cli args:
    if options_compile is not None:
        user_config.compile.options = UserCompileOptions(**{
            **user_config.compile.options,
            **options_compile
        });

    # overwrite user config with user cli args:
    if options_stamp is not None:
        if user_config.stamp is None:
            user_config.stamp = UserStampBlock(options=options_stamp);
        user_config.stamp.options = {
            **user_config.stamp.options,
            **options_stamp
        };

    # overwrite:
    config.PATHS.file_start = user_config.compile.options.root;
    config.PATHS.file_output = user_config.compile.options.output;

    log_info('READ CONFIG COMPLETE');
    return user_config;
