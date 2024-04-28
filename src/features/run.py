#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This file contains the main process.
If called from e.g. cli.py or api.py, must initialise all paths.
'''

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ..thirdparty.misc import *

from ..core.logging import *
from ..models.application import *
from . import feature_transpile

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'process',
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def process(
    feature: EnumFeatures,
    path_config: str,
    compileoptions: dict = {},
    parameters: dict = {},
):
    '''
    Hub for running all features.
    '''
    log_console(
        dedent(
            '''
        +--------------------+
        |     \033[32;1m(PH(p)y)tex\033[0m    |
        +--------------------+
        '''
        )
    )
    match feature:
        case EnumFeatures.TRANSPILE as feature:
            feature_transpile.endpoint(
                feature=feature,
                path_config=path_config,
                compileoptions=compileoptions,
                parameters=parameters,
            )

        case _ as ft if isinstance(feature, EnumFeatures):
            raise ValueError(f'No method developed for {ft.value}')

        case _ as value:
            raise ValueError(f'No method developed for {value}')
    return
