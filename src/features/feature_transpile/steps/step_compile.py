#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ....thirdparty.misc import *
from ....thirdparty.system import *
from ....thirdparty.types import *

from ....core.logging import *
from ....setup import *
from ....models.user import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'step_compile',
]

# ----------------------------------------------------------------
# METHOD: step transpile python to latex
# ----------------------------------------------------------------


@echo_function(tag='STEP TRANSPILE (python -> latex)', level=LOG_LEVELS.INFO, close=True)
def step_compile(cfg_user: UserConfig):
    options = cfg_user.compile.options

    execute_transpiled_code(options.transpiled, options.output)
    remove_file_if_exists(options.transpiled)
    return


# ----------------------------------------------------------------
# SECONDARY METHODS
# ----------------------------------------------------------------


def execute_transpiled_code(path_from: str, path_to: str):
    try:
        cmd = re.split(r'\s+', python_command()) + [path_from]
        log_info(f"CALL < \033[94;1m{' '.join(cmd)}\033[0m >")
        pipe_call(cmd)
    except:
        log_fatal(
            'An error occurred during (python -> latex -> pdf) conversion.',
            f'  - Consult the error logs and the script \033[1m{path_from}\033[0m for more information.',
            f'  - Partial output may also be found in \033[1m{path_to}\033[0m.',
        )
    return
