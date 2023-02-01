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

# NOTE: need to import this way to avoid conflicts
import src.models.config;
import src.models.user;

from src.setup import *;
from src.core.log import *;
from src.core.utils import *;
from src.models.internal import *;

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
    options_transpile: Optional[dict] = None,
    options_stamp: Optional[dict] = None,
) -> src.models.user.UserConfig:
    log_info('READ CONFIG STARTED');

    user_config = load_user_config(file_config);

    if user_config.compile is not None:
        log_warn(dedent(f'''
        Please use \x1b[1mtranspile:\x1b[0m instead of \x1b[1mcompile:\x1b[0m in the config file!
        Furthermore structure this block in the configuration file as follows:

          {config.PATHS.file_config} contents
          \x1b[1m--------------------------------
          ...
          transpile:
            options:
              ...
          ...
          --------------------------------\x1b[0m
        '''));

    user_config.transpile = clean_up_compile_block(
        block = user_config.transpile or user_config.compile,
        options = options_transpile,
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

    assert isinstance(user_config.transpile, src.models.user.UserTranspileBlock);
    assert isinstance(user_config.transpile.options, src.models.user.UserTranspileOptions);

    update_config(
        transpilation = user_config.transpile.options,
        stamp = user_config.stamp,
        parameters = user_config.parameters,
    );

    log_info('READ CONFIG COMPLETE');
    return user_config;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS: config update
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def update_config(
    transpilation: src.models.user.UserTranspileOptions,
    stamp: Optional[src.models.user.UserStampBlock],
    parameters: Optional[src.models.user.UserParametersBlock],
) -> None:
    assert transpilation.root != transpilation.output, \
        'transpile > options > root and transpile > options > output MUST be different!';

    config.PATHS.file_start = transpilation.root;
    config.PATHS.file_output = transpilation.output;

    if stamp:
        config.PATHS.overwrite_stamp = stamp.overwrite;
        config.PATHS.file_stamp = stamp.file;

    if parameters:
        config.PATHS.overwrite_params = parameters.overwrite;
        import_name = parameters.file;
        parts = re.split(pattern=r'\.', string=import_name);
        config.PATHS.import_params = import_name;
        config.PATHS.file_params_py = os.path.join(*parts);

    config.TRANSPILATION = src.models.config.TranspileOptions(**{
        **config.TRANSPILATION.dict(),
        # NOTE: need to convert enums:
        **transpilation.dict(exclude={
            'comments',
        }),
        'comments': transpilation.comments.value,
        # NOTE: alternative, but unnecessary:
        # 'comments': src.models.config.EnumCommentsOption(transpilation.comments.value);
    });

    # set spacing options
    if transpilation.tabs:
        config.TRANSPILATION.indent_character = '\t';
        config.TRANSPILATION.indent_character_re = r'\t';
    else:
        n = transpilation.spaces;
        config.TRANSPILATION.indent_character = n * ' ';
        config.TRANSPILATION.indent_character_re = n * ' ';

    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS: cleanup
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def clean_up_compile_block(
    block: Optional[src.models.user.UserTranspileBlock | src.models.user.UserTranspileOptions],
    options: Optional[dict]
) -> src.models.user.UserTranspileBlock:
    '''
    Forces compile options to be defined, and potentially overrides options with cli arguments.
    '''
    if block is None:
        block = src.models.user.UserTranspileBlock(options=options);

    if not isinstance(block, src.models.user.UserTranspileBlock):
        block = src.models.user.UserTranspileBlock(options=block);

    if options is not None:
        block.options = src.models.user.UserTranspileOptions(**{
            **block.options,
            **options
        });
    return block;

def clean_up_parameters_block(
    block: Optional[src.models.user.UserParametersBlock],
    options: Optional[dict]
) -> src.models.user.UserParametersBlock:
    '''
    Forces parameters options to be defined, if options provided via cli arguments.
    '''
    if options is None:
        return block;

    if block is None:
        block = src.models.user.UserParametersBlock(options=options);

    block.options = { **block.options, **options };

    return block;

def clean_up_stamp_block(
    block: Optional[src.models.user.UserStampBlock],
    options: Optional[dict]
) -> src.models.user.UserStampBlock:
    '''
    Forces stamp options to be defined, if options provided via cli arguments.
    '''
    if options is None:
        return block;

    if block is None:
        block = src.models.user.UserStampBlock(options=options);
    block.options = { **block.options, **options };

    return block;
