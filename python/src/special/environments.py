#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.typing import *;
from src.special.methods import *;
from src.special.macros import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'LatexEnvironment',
    'LatexEnvironments',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: LatexEnvironment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LatexEnvironment:
    name:       str;
    overwrite:  bool;
    definition: str;
    depth:      int;
    storage:    List[dict]; # for local storage inside an environment
    __begin:    LatexMacro;
    __end:      LatexMacro;

    def __init__(self):
        self.storage = [];
        self.depth   = -1
        return;

    @property
    def begin(self) -> LatexMacro:
        return self.__begin;

    @begin.setter
    def begin(self, m: LatexMacro):
        _m = m.clone();
        def __use(*args, **kwargs):
            self.pushstorage();
            return m.use(*args, **kwargs);
        _m.use = __use;
        self.__begin = _m;

    @property
    def end(self) -> LatexMacro:
        return self.__end;

    @end.setter
    def end(self, m: LatexMacro):
        _m = m.clone();
        def __use(*args, **kwargs):
            self.popstorage();
            return m.use(*args, **kwargs);
        _m.use = __use;
        self.__end = _m;

    def __len__(self):
        return len(self.storage);

    def pushstorage(self):
        n = self.depth;
        self.depth = max(n + 1, 0);
        self.storage.append(dict());

    def popstorage(self):
        n = self.depth;
        self.depth = max(n - 1, -1);
        if n >= 0:
            self.storage = self.storage[:n];

    def save(self, key: str, value):
        if self.depth < 0:
            return;
        self.storage[self.depth][key] = value;

    def load(self, key: str):
        if self.depth < 0 or self.depth >= self.__len__():
            return;
        kw = self.storage[self.depth];
        return kw[key] if key in kw else None;
    pass;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: LatexEnvironments
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LatexEnvironments:
    __objects: Dict[str, LatexEnvironment];
    definescheme:   Callable[..., str];
    usebeginscheme: Callable[..., Callable[..., str]];
    useendscheme: Callable[..., Callable[..., str]];

    def __init__(self):
        self.__objects = dict();

        ## create native LaTeX macro definition:
        def definescheme(name: str, overwrite: bool = False, n: int = 0, begincontents: List[str] = [], endcontents: List[str] = [], **kwargs) -> str:
            beginlines = joinlines(begincontents, relax=True, percent=True);
            endlines   = joinlines(endcontents, relax=True, percent=True);
            opt        = dict(name=name, n=n, beginlines=beginlines, endlines=endlines);
            ovr        = '\\newenvironment';
            if overwrite:
                ovr = '\\providecommand{{\\{name}}}{{}}\n\\renewenvironment'.format(**opt);
            if n > 0:
                return ovr + '{{\\{name}}}[{n}]{{{beginlines}}}{{{endlines}}}'.format(**opt);
            else:
                return ovr + '{{\\{name}}}{{{beginlines}}}{{{endlines}}}'.format(**opt);

        ## create method to call native  LaTeX-macro:
        def usebeginscheme(env: LatexEnvironment, name: str, n: int = 0, keys: List[str] = [], **kwargs) -> Callable[..., str]:
            def __usescheme(*_, **__) -> str:
                _  = (list(_) + ['' for _ in range(n)])[:n];
                _ += [__[___] if _ in __ else '' for ___ in keys];
                _  = ''.join(['{{{}}}'.format(___) for ___ in _]);
                return '\\begin{{{name}}}{args}'.format(name=name, args=_);
            return __usescheme;

        ## create method to call native  LaTeX-macro:
        def useendscheme(env: LatexEnvironment, name: str, n: int = 0, keys: List[str] = [], **kwargs) -> Callable[..., str]:
            def __usescheme(*_, **__) -> str:
                return '\\end{{{name}}}'.format(name=name);
            return __usescheme;

        self.definescheme   = definescheme;
        self.usebeginscheme = usebeginscheme;
        self.useendscheme   = useendscheme;
        pass;

    def __contains__(self, x):
        return isinstance(x, str) and x in self.__objects;

    def __iter__(self):
        for alias in self.__objects:
            yield alias, self.__objects[alias];

    def get(self, alias: str) -> LatexEnvironment:
        if not self.__contains__(alias):
            raise AttributeError('LATEX environment \033[1m{}\033[0m not set'.format(alias));
        return self.__objects[alias];

    def begin(self, alias: str, *args, **kwargs) -> str:
        env = self.get(alias);
        return env.begin.use(*args, **kwargs);

    def end(self, alias: str, *args, **kwargs) -> str:
        env = self.get(alias);
        return env.end.use(*args, **kwargs);

    # Intention: should creates explicit LaTeX definition. This can be customised.
    def set(
        self,
        alias:     str,
        name:      Union[str, None]                     = None,
        silent:    bool                                 = False, # True <--> implicit definition, i.e. no latex macro created.
        overwrite: bool                                 = False, # True <--> if explicit latex env exists, overwrite it.
        n:         int                                  = 0,
        keys:      List[str]                            = [],
        begin:     Union[Callable[..., str], List[str]] = [],
        end:       Union[Callable[..., str], List[str]] = []
    ):
        _ = LatexEnvironment();
        _.name       = name if isinstance(name, str) else alias;
        _.overwrite  = overwrite;
        __beginmacro = LatexMacro();
        __endmacro   = LatexMacro();

        if silent:
            if not isinstance(begin, function) or not isinstance(end, function):
                raise TypeError('begin/end arguments must be callable.');
            __beginmacro.use = begin;
            __endmacro.use   = end;
        else:
            if not isinstance(begin, list) or not isinstance(end, list):
                raise TypeError('begin/end arguments must be lists of strings.');
            _.definition     = self.definescheme(name=_.name, overwrite=overwrite, n=n + len(keys), begincontents=begin, endcontents=end);
            __beginmacro.use = self.usebeginscheme(_, _.name, n, keys);
            __endmacro.use   = self.useendscheme(_, _.name, n, keys);

        _.begin = __beginmacro;
        _.end   = __endmacro;
        self.__objects[alias] = _;
        return;
    pass;
