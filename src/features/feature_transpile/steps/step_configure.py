#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...._core.logging import *
from ...._core.utils.basic import *
from ....models.enums import *
from ....models.transpilation import *
from ....models.user import *
from ....queries import user
from ....setup import *
from ....thirdparty.misc import *
from ....thirdparty.system import *
from ....thirdparty.types import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "step_configure",
]

# ----------------------------------------------------------------
# GLOBAL VARIABLES
# ----------------------------------------------------------------

#

# ----------------------------------------------------------------
# METHOD: step get config
# ----------------------------------------------------------------


@echo_function(tag="STEP READ CONFIG", level="INFO", close=True)
def step_configure(
    path_config: str,
    compileoptions: dict = {},
    parameters: dict = {},
) -> UserConfig:
    # get configuration file
    path_config = path_config or user.locate_user_config()
    cfg_user = user.load_user_config(path_config)

    # overwrite config compile-options via cli-parameters
    if len(compileoptions) > 0:
        options = cfg_user.compile.options
        raw = options.model_dump() | compileoptions
        options = UserConfigPartCompileOptions.model_validate(raw)
        cfg_user.compile.options = options

    # overwrite config parameters-options via cli-parameters
    if len(parameters) > 0:
        options = cfg_user.parameters.options
        raw = (options or {}) | parameters
        cfg_user.parameters.options = raw

    # handle parts of config file
    handle_part_compile(cfg_user.compile.options)
    return cfg_user


# ----------------------------------------------------------------
# SECONDARY METHODS
# ----------------------------------------------------------------


def handle_part_compile(options: UserConfigPartCompileOptions):
    if options.tabs:
        user.setting_indent_character.set("\t")
        user.setting_indent_character_re.set(r"\t")
    else:
        user.setting_indent_character.set(" " * options.spaces)
        user.setting_indent_character_re.set(" " * options.spaces)

    file_input = os.path.abspath(options.root)
    file_output = os.path.abspath(options.output)

    assert (
        file_input != file_output
    ), "The output and start ('root'-attribute in config) paths must be different!"
    return
