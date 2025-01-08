#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging

from ..._core.logging import *
from ...models.application import *
from ...setup import *
from ...thirdparty.misc import *
from .steps import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "endpoint",
]

# ----------------------------------------------------------------
# FEATURE
# ----------------------------------------------------------------


@echo_function(tag="FEATURE {feature.value}", level="INFO", close=True)
def endpoint(
    feature: EnumFeatures,
    path_config: str,
    compileoptions: dict = {},
    parameters: dict = {},
):
    cfg_user = step_configure(path_config, compileoptions=compileoptions, parameters=parameters)
    if cfg_user.ignore:
        logging.info("\033[32;1m(PH(p)y)tex\033[0m transpilation will be skipped.")
        return

    step_create(cfg_user)
    step_transpile(cfg_user)

    if cfg_user.compile.options.debug:
        path = cfg_user.compile.options.transpiled
        logging.info(f"The result of transpilation can be viewed in \033[1m{path}\033[0m")
        return

    step_compile(cfg_user)
    return
