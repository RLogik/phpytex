#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import json;
from lazy_load import lazy;
from typing import Any;
from typing import Optional;
from yaml import add_constructor;
from yaml import load as yaml_load;
from yaml import Loader as YamlLoader;
from yaml import FullLoader as YamlFullLoader;
from yaml import add_path_resolver as yaml_add_path_resolver;
from yaml.nodes import SequenceNode as YamlSequenceNode;

from functools import wraps;
from typing import Callable;
from typing import TypeVar;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODIFICATIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def json_load_safe(text: Optional[str]) -> Optional[dict[str, Any]]:
    if text is None:
        return None;
    try:
        object = json.loads(text);
        if not isinstance(object, dict):
            object = None;
        return object;
    except:
        return None;

def yaml_add_constructor(tag: str, attach: bool = True):
    '''
    Returns a decorator, which, when applied to a method,
    attaches the method as a constructor.

    @inputs
    - `tag` - name of constructor
    - `attach` -  <bool> `True` => perform attachment immediately

    @returns
    - If `attach == True`, application of the decorator forcibly performs the attachment.
    - If `attach == False`, returns a wrapped method, which performs the attachement, when called.
    '''
    T = TypeVar('T');
    def dec(method: Callable[[YamlLoader, YamlSequenceNode], T]) -> Callable[[], None]:
        '''
        Attaches the method as a constructor.
        '''

        if attach:
            add_constructor(tag=tag, constructor=method);

        @wraps(method)
        def wrapped_method() -> None:
            if not attach:
                add_constructor(tag=tag, constructor=method);
            return;

        return wrapped_method;
    return dec;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'YamlFullLoader',
    'YamlLoader',
    'YamlSequenceNode',
    'add_constructor',
    'json',
    'json_load_safe',
    'lazy',
    'yaml_add_constructor',
    'yaml_add_path_resolver',
    'yaml_load',
];
