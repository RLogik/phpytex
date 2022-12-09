#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.setup import *;
from src.core.log import *;
from src.core.utils import *;
from src.models.user import *;
from src.steps import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'endpoint_run',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENDPOINT run phpytex
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def endpoint_run(
    file_config: Optional[str] = None,
    options_parameters: Optional[dict] = None,
    options_transpile: Optional[dict] = None,
    options_stamp: Optional[dict] = None,
) -> None:
    '''
    Runs transpiler
    '''
    log_info(dedent('''\n
        +--------------------+
        |     \033[32;1m(PH(p)y)tex\033[0m    |
        +--------------------+
    '''));

    user_config = step_configure(
        file_config = file_config,
        options_parameters = options_parameters,
        options_transpile = options_transpile,
        options_stamp = options_stamp,
    );

    step_create(user_config = user_config);
    step_transpile();
    if config.TRANSPILATION.debug:
        log_info(f'The result of transpilation can be viewed in \033[1m{config.PATHS.file_transpiled}\033[0m');
        return;
    step_compile();
    return;
