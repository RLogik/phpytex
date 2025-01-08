#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ...thirdparty.system import *
from ...thirdparty.maths import *
from ...thirdparty.types import *

from ..._core.utils.basic import *
from ...models.internal import *
from ...models.transpilation import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'EXPORT_VARS',
    'setting_indent_character',
    'setting_indent_character_re',
]

# ----------------------------------------------------------------
# GLOBAL VARIABLES
# ----------------------------------------------------------------

setting_indent_character = FinalProperty[str]()
setting_indent_character_re = FinalProperty[str]()
EXPORT_VARS: dict[str, tuple[Any, str]] = {}

# ----------------------------------------------------------------
# METHODS: get/set
# ----------------------------------------------------------------


def setExportVarsKeyValue(key: str, value: Any, codedvalue: str):
    EXPORT_VARS[key] = (value, codedvalue)
    return
