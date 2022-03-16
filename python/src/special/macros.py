#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any;
from typing import Callable;
from typing import Dict;
from typing import List;

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

class LatexMacro(object):
    alias: str;
    anon: bool;
    overwrite: bool;
    definition: str;
    usage: Callable[..., str];

    def __init__(
        self,
        alias: str,
        anon: bool,
        usage: Callable[..., str],
        definition: str = '',
        overwrite: bool = False,
    ):
        self.alias = alias;
        self.anon = anon;
        self.overwrite = overwrite;
        self.definition = definition;
        self.usage = usage;
        return;

    def clone(self):
        return LatexMacro(
            alias      = self.alias,
            anon       = self.anon,
            overwrite  = self.overwrite,
            definition = self.definition,
            usage      = self.usage,
        );

    def getDefinition(self) -> str:
        return '' if self.anon else self.definition;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: LatexMacros
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LatexMacros(object):
    _objects:         Dict[str, LatexMacro];

    def __init__(self):
        self._objects = dict();
        pass;

    def __contains__(self, x):
        return isinstance(x, str) and x in self._objects;

    def __iter__(self):
        for alias in self._objects:
            yield alias, self._objects[alias];

    def get(self, alias: str) -> LatexMacro:
        if self.__contains__(alias):
            return self._objects[alias];
        raise AttributeError('LATEX macro \033[1m{}\033[0m not set.'.format(alias));

    def get_definition(self, alias: str) -> str:
        return self.get(alias).getDefinition();

    def use(self, alias: str, *args, **kwargs) -> str:
        return self.get(alias).usage(*args, **kwargs);

    def add(
        self,
        alias:     str,
        contents:  str,
        n:         int       = 0,
        keys:      List[str] = [],
        overwrite: bool      = False,
        multiline: bool      = True,
        name:      Any       = None,
    ):
        '''
        ## Create explicit LaTeX definition ##

        @inputs
        - `alias`     - how command should be referred to in python.
        - `name`      - how command should be named to in LaTeX (defaults to alias, if not given).
        - `overwrite` - <bool> force overwrite LaTeX definition if exists.
        - `multiline` - <bool> whether LaTeX-command should allow par breaks.
        - `n`         - number of unnamed arguments in macro
        - `keys`      - named arguments in macro
        - `contents`  - lines of content in explicit LaTeX deinition

        ## Example ##

        ```py
        macros = LatexMacros();
        macros.add(alias='tree-stats', name='showTreeStats',
            n=1, keys=['age', 'colour'],
            contents=r"""
            \\begin{#1}
                \\item The tree is \\textit{age} years old.
                \\item The tree is \\textit{colour}.
            \\end{#1}
            """,
        );
        ```
        Calling
        ```coffee
        <<< macros.get_definition('tree-stats'); >>>
        ```
        displays
        ```tex
        \\providecommand{\\showTreeStats}{}
        \\renewcommand{\\showTreeStats}[3]{%
            \\begin{#1}\\relax%
                \\item The tree is \\textit{#2} years old.\\relax%
                \\item The tree is \\textit{#3}.\\relax%
            \\end{#1}\\relax%
        }
        ```
        in .tex files, and
        ```coffee
        <<< macros.use('tree-stats', 'itemize', colour='brown', age=387); >>>
        ```
        displays
        ```tex
        \\showTreeStats{itemize}{387}{brown}
        ```
        in .tex files.
        '''
        contents, n = anonymise_arguments(contents, n, keys);
        ## create definition + usage:
        name = name if isinstance(name, str) else alias;
        definition = createMacroDefinition(name=name, overwrite=overwrite, multiline=multiline, n=n, contents=contents);
        usage = createMacroUsage(name=name, n=n, keys=keys);
        ## add new macro in dictionary:
        self._objects[alias] = LatexMacro(
            alias      = alias,
            anon       = False,
            overwrite  = overwrite,
            usage      = usage,
            definition = definition,
        );
        return;

    def add_anon(
        self,
        alias: str,
        usage: Callable[..., str],
    ):
        '''
        ## Create anonymous LaTeX definition ##

        @inputs
        - `alias` - how command should be referred to in python.
        - `usage` - implicit method

        ## Example ##

        ```py
        macros = LatexMacros();
        macros.add_anon(alias='filter-limit',
            usage = lambda F, var: \
                r"\\mathop{{ \\mathcal{{{F}}}\\text{-}\\lim_{{{var}}}} }}".format(F=F, var=var)
        );
        ```
        Using
        ```coffee
        <<< macros.getDefinition('filter-limit'); >>>
        ```
        displays an empty line in .tex files. And
        ```coffee
        <<< macros.use('filter-limit', var='n', F='G'); >>>
        ```
        displays
        ```tex
        \\mathop{ \\mathcal{G}\\text{-}\\lim_{n} }
        ```
        in .tex files.
        '''
        self._objects[alias] = LatexMacro(alias=alias, anon=True, usage=usage);
        return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def createMacroDefinition(
    name:      str,
    overwrite: bool,
    multiline: bool,
    n:         int,
    contents:  str,
) -> str:
    '''
    Creates native LaTeX macro definition.
    '''
    # split contents into lines and trim empty lines:
    lines = join_lines(clean_lines(contents), relax=True, percent=True);
    ## create latex command:
    options = dict(
        name  = name,
        n     = n,
        lines = lines,
        multi = '' if multiline else '*',
    );
    if overwrite:
        return dedentIgnoreFirstAndLast('''
            \\providecommand{{\\{name}}}{{}}
            \\renewcommand{multi}{{\\{name}}}[{n}]{{{lines}}}
        ''').format(**options)
    return dedentIgnoreFirstAndLast('''
        \\newcommand{multi}{{\\{name}}}[{n}]{{{lines}}}
    ''').format(**options);

## creates usage to call an explicitly created LaTeX-macro:
def createMacroUsage(name: str, n: int, keys: List[str]) -> Callable[..., str]:
    '''
    Creates usage function for explicitly defined LaTeX macro.
    '''
    def usage(*_, **__) -> str:
        args_string = convert_args_to_latex_args_as_string(n=n, keys=keys, args=_, kwargs=__);
        return '\\{name}{args}'.format(name=name, args=args_string);
    return usage;
