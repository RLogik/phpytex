#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "get_root_path",
    "get_source_path",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

_source = os.path.dirname(__file__)
_root = os.path.dirname(_source)

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def get_path(root: str, *parts: str) -> str:
    return root if len(parts) == 0 else os.path.join(root, *parts)


def get_root_path(*parts: str) -> str:
    return get_path(_root, *parts)


def get_source_path(*parts: str) -> str:
    return get_path(_source, *parts)
