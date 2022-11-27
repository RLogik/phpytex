#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from dataclasses import asdict;
from dataclasses import dataclass;
from dataclasses import field;
from dataclasses import Field;
from dataclasses import MISSING;
from functools import partial;
from functools import reduce;
from functools import wraps;
from itertools import chain as itertools_chain;
from itertools import product as itertools_product;
from lazy_load import lazy;
from operator import itemgetter;
from pydantic import BaseModel;
# cf. https://github.com/mplanchard/safetywrap
from safetywrap import Err;
from safetywrap import Nothing;
from safetywrap import Ok;
from safetywrap import Option;
from safetywrap import Result;
from safetywrap import Some;
from typing import Callable;
from typing import ParamSpec;
from typing import TypeVar;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODIFICATIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ARGS = ParamSpec('ARGS');
T = TypeVar('T');

def make_lazy(method: Callable[ARGS, T]) -> Callable[ARGS, T]:
    '''
    Decorates a method and makes it return a lazy-load output.
    '''
    @wraps(method)
    def wrapped_method(**kwargs) -> T:
        return lazy(partial(method), **kwargs);
    return wrapped_method;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'asdict',
    'BaseModel',
    'dataclass',
    'Err',
    'Field',
    'field',
    'itemgetter',
    'itertools_chain',
    'itertools_product',
    'make_lazy',
    'MISSING',
    'Nothing',
    'Ok',
    'Option',
    'partial',
    'reduce',
    'Result',
    'Some',
    'wraps',
];
