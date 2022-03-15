#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.typing import *;
from src.special.methods import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'LatexMacro',
    'LatexMacros',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: LatexMacro
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LatexMacro:
    name: str;
    overwrite: bool;
    definition: str;
    use: Callable[..., str];

    def clone(self):
        m = LatexMacro();
        for _ in ['name', 'overwrite', 'definition', 'use']:
            if hasattr(self, _):
                setattr(m, _, getattr(self, _));
        return m;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: LatexMacros
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LatexMacros:
    __objects: Dict[str, LatexMacro];
    definescheme: Callable[..., str];
    usescheme:    Callable[..., Callable[..., str]];

    def __init__(self):
        self.__objects = dict();

        ## create native LaTeX macro definition:
        def definescheme(name: str, overwrite: bool = False, n: int = 0, contents: List[str] = [], **kwargs) -> str:
            lines  = joinlines(contents, relax=True, percent=True);
            opt    = dict(name=name, n=n, lines=lines);
            cmd    = '\\providecommand{{\\{name}}}{{}}\n\\renewcommand*'.format(**opt) if overwrite else '\\newcommand*';
            if n > 0:
                return cmd + '{{\\{name}}}[{n}]{{{lines}}}'.format(**opt);
            else:
                return cmd + '{{\\{name}}}{{{lines}}}'.format(**opt);

        ## create method to call native  LaTeX-macro:
        def usescheme(name: str, n: int, keys: List[str], **kwargs) -> Callable[..., str]:
            def __usescheme(*_args, **_kwargs) -> str:
                values  = (list(_args) + ['' for _ in range(n)])[:n];
                values += [(_kwargs[_key] if _key in _kwargs else '') for _key in keys];
                values  = ''.join(['{{{}}}'.format(_val) for _val in values]);
                return '\\{name}{args}'.format(name=name, args=values);
            return __usescheme;

        self.definescheme = definescheme;
        self.usescheme    = usescheme;
        pass;

    def __contains__(self, x):
        return isinstance(x, str) and x in self.__objects;

    def __iter__(self):
        for alias in self.__objects:
            yield alias, self.__objects[alias];

    def __getitem__(self, alias: str) -> Callable[..., str]:
        if alias in self.__objects:
            return self.__objects[alias].use;
        else:
            raise AttributeError('LATEX macro \033[1m{}\033[0m not set.'.format(alias));

    # def __getattr__(self, alias: str) -> Callable[..., str]:
    def get(self, alias: str) -> LatexMacro:
        if not alias in self.__objects:
            raise AttributeError('LATEX macro \033[1m{}\033[0m not set.'.format(alias));
        return self.__objects[alias]

    def use(self, alias: str, *args, **kwargs) -> str:
        return self.get(alias).use(*args, **kwargs);

    # Intention: should create explicit LaTeX definition. This can be customised.
    def set(
        self,
        alias:     str,
        name:      Union[str, None]   = None,
        silent:    bool               = False, # True <--> implicit definition, i.e. no latex macro created.
        overwrite: bool               = False, # True <--> if explicit latex macro exists, overwrite it.
        n:         int                = 0,
        keys:      List[str]          = [],
        contents:  List[str]          = [],
        use:       Callable[..., str] = lambda: ''
    ):
        _ = LatexMacro();
        _.name      = name if isinstance(name, str) else alias;
        _.overwrite = overwrite;

        if silent:
            _.use        = use;
        else:
            _.definition = self.definescheme(name=name, overwrite=overwrite, n=n + len(keys), contents=contents);
            _.use        = self.usescheme(name, n, keys);

        self.__objects[alias] = _;
        return;
    pass;
