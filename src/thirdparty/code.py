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
# import inspect;
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
from typing import ClassVar;
from typing import Callable;
from typing import ParamSpec;
from typing import TypeVar;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODIFICATIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ARGS = ParamSpec('ARGS');
C = ClassVar('C');
T = TypeVar('T');

# def base_signature(cls: Callable):
#     '''
#     Decorates a method of a superclass to preserve the signature of the base class.
#     '''
#     def dec(func: Callable) -> Callable:
#         # func.__doc__ = inspect.doc(cls); # <- does not exist.
#         name = func.__name__;
#         if hasattr(cls, func.__name__):
#             func.__signature__ = inspect.signature(cls);
#         return func;
#     return dec;

def final_property(method: Callable[[C], T]) -> Callable[[C], T]:
    '''
    Decorates a `@property`-decorated methods in a class,
    so that method is computed at most once.

    **Note:** If using in a class for a property named _e.g._ `info`,
    ensure that you do not define a class attribute called `_info`.
    This decorater creates an attribute with this name,
    in order to keep track of whether the property has been created.

    ## USAGE ##
    Use decorater _below_ the `@property`-decorator.
    ```py
    # file: main.py
    from dataclasses import field;

    @dataclass
    class Element:
        name: str = field();
        weight: float = field();

        @property
        @final_property
        def info(self):
            # add side effect to see whether this method is called.
            print('computed output');
            return f'Element {name}, {weight}u.';

    if __name__ == '__main__':
        # create instance and use property:
        m = Element(name='Argon', weight=39.948);
        print(m.info);
        print(m.info);
    ```
    ouput of script:
    ```bash
    ... $ python3 main.py
    ... $
    computed output
    Element Argon, 39.948u.
    Element Argon, 39.948u.
    ```
    _i.e._ the property is computed at most once.
    '''
    @wraps(method)
    def wrapped_method(cls: C) -> T:
        # name of method
        name = method.__name__;
        # use as private attribute name
        private_name = f'_{name}';
        # compute value ONCE only:
        if not hasattr(cls, private_name):
            value = method(cls);
            setattr(cls, private_name, value);
        return getattr(cls, private_name);
    return wrapped_method;

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
    # 'base_signature',
    'BaseModel',
    'dataclass',
    'Err',
    'Field',
    'field',
    'final_property',
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
