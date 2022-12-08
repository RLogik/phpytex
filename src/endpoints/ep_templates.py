#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.system import *;

from src.setup import *;
from src.core.utils import *;
from src.core.log import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'endpoint_example',
    'endpoint_template',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENDPOINT template of config file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def endpoint_template():
    log_info(dedent(f'''\n
        +--------------------+
        |     \033[32;1m(PH(p)y)tex\033[0m    |
        +--------------------+

        generate config file \x1b[1m{config.PATHS.file_config}\x1b[0m...
    '''));
    lines = str(TEMPLATE_CONFIG);
    write_text_file(path=config.PATHS.file_config, lines=lines);
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENDPOINT example of config file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def endpoint_example():
    log_info(dedent(f'''\n
        +--------------------+
        |     \033[32;1m(PH(p)y)tex\033[0m    |
        +--------------------+

        generate config file \x1b[1m{config.PATHS.file_config}\x1b[0m...
    '''));
    lines = str(TEMPLATE_EXAMPLE);
    write_text_file(path=config.PATHS.file_config, lines=lines);
    return;
