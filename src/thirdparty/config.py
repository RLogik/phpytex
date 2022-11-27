#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import json;
from lazy_load import lazy;
from typing import Any;
from typing import Callable;
from yaml import add_constructor;
from yaml import load as yaml_load;
from yaml import Loader as yaml_Loader;
from yaml import FullLoader as yaml_FullLoader;
from yaml import add_path_resolver as yaml_add_path_resolver;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODIFICATIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def json_load_safe(
    text: Any,
    default_factory: Callable[[], dict] = dict
) -> dict[str, Any]:
    try:
        if isinstance(text, str):
            return json.loads(text);
    except:
        pass;
    return default_factory();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'add_constructor',
    'json',
    'json_load_safe',
    'lazy',
    'yaml_FullLoader',
    'yaml_Loader',
    'yaml_add_path_resolver',
    'yaml_load',
];
