#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from . import assets
from . import config

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

FUNCTION_NAME_MAIN = "____phpytex_main"
FUNCTION_NAME_FILE = "____phpytex_generate_file"
FUNCTION_NAME_PRE = "____phpytex_generate_pre"

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "FUNCTION_NAME_FILE",
    "FUNCTION_NAME_MAIN",
    "FUNCTION_NAME_PRE",
    "assets",
    "config",
]
