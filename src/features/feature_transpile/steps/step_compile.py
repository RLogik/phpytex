#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging

from ...._core.logging import *
from ....models.user import *
from ....setup import *
from ....thirdparty.misc import *
from ....thirdparty.system import *
from ....thirdparty.types import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "step_compile",
]

# ----------------------------------------------------------------
# METHOD: step transpile python to latex
# ----------------------------------------------------------------


@echo_function(
    tag="STEP TRANSPILE/COMPILE (phpytex -> [py -> tex -> pdf])",
    level="INFO",
    close=True,
)
def step_compile(cfg_user: UserConfig):
    options = cfg_user.compile.options
    execute_transpiled_code(options)
    remove_file_if_exists(options.transpiled)
    return


# ----------------------------------------------------------------
# SECONDARY METHODS
# ----------------------------------------------------------------


def execute_transpiled_code(options: UserConfigPartCompileOptions):
    try:
        path_from = options.transpiled
        path_to = options.output
        python_cmd = options.python_path or python_command()
        cmd = [*re.split(r"\s+", python_cmd), path_from]
        logging.info(f"CALL < \033[94;1m{' '.join(cmd)}\033[0m >")
        pipe_call(cmd)

    except Exception as err:
        message = "\n".join(
            [
                "An error occurred during (phpytex -> [py -> tex -> pdf]) conversion.",
                f"  - Consult the error logs and the script \033[1m{path_from}\033[0m for more information.",
                f"  - Partial output may also be found in \033[1m{path_to}\033[0m.",
            ]
        )
        err.add_note(message)
        raise err
