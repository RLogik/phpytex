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
from src.special.storage import *;
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
    alias: str;
    anon: bool;
    overwrite: bool;
    definition: str;
    begin: LatexMacro;
    end:   LatexMacro;

    def __init__(
        self,
        alias:      str,
        anon:       bool,
        begin:      LatexMacro,
        end:        LatexMacro,
        definition: str  = '',
        overwrite:  bool = False,
    ):
        self.alias = alias;
        self.anon = anon;
        self.overwrite = overwrite;
        self.definition = definition;
        self.begin = begin;
        self.end = end;
        return;

    def clone(self):
        return LatexEnvironment(
            alias      = self.alias,
            anon       = self.anon,
            overwrite  = self.overwrite,
            definition = self.definition,
            begin      = self.begin.clone(),
            end        = self.end.clone(),
        );

    def getDefinition(self) -> str:
        return '' if self.anon else self.definition;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: LatexEnvironments
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LatexEnvironments:
    _objects: Dict[str, LatexEnvironment];
    storage:  Storage; # for local storage inside an environment

    def __init__(self):
        self._objects = dict();
        return;

    def __contains__(self, x):
        return isinstance(x, str) and x in self._objects;

    def __iter__(self):
        for alias in self._objects:
            yield alias, self._objects[alias];
        return;

    def get(self, alias: str) -> LatexEnvironment:
        if self.__contains__(alias):
            return self._objects[alias];
        raise AttributeError('LATEX environment \033[1m{}\033[0m not set'.format(alias));

    def get_definition(self, alias: str) -> str:
        return self.get(alias).definition;

    def begin(self, alias: str, *args, **kwargs) -> str:
        self.storage.push(kwargs);
        return self.get(alias).begin.usage(*args, **kwargs);

    def end(self, alias: str) -> str:
        self.storage.pop();
        return self.get(alias).end.usage();

    # Intention: should creates explicit LaTeX definition. This can be customised.
    def add(
        self,
        alias:      str,
        begin:      str,
        end:        str,
        n:          int       = 0,
        keys:       List[str] = [],
        overwrite:  bool      = False,
        multiline:  bool      = True,
        name:       Any       = None,
    ):
        '''
        ## Create explicit LaTeX environment definition ##

        @inputs
        - `alias`     - how command should be referred to in python.
        - `name`      - how command should be named to in LaTeX (defaults to alias, if not given).
        - `overwrite` - <bool> force overwrite LaTeX environment if exists.
        - `multiline` - <bool> whether LaTeX-command should allow par breaks.
        - `n`         - number of unnamed arguments in `\begin{...}`
        - `keys`      - named arguments in `\begin{...}`
        - `begin`     - lines of content in explicit LaTeX deinition for `\begin{...}`
        - `end`       - lines of content in explicit LaTeX deinition for `\end{...}`

        NOTE: The `\end{...}`-command cannot take any arguments.

        ## Example ##

        ```py
        environments = LatexEnvironments();
        environments.add_anon(alias='maths-block', name='maths', overwrite=True,
            n=0, keys=['halign', 'valign'],
            begin=r"""
                \\begin{math}
                \\begin{array}[valign]{halign}
            """,
            end = r"""
                \\end{array}
                \\end{math}
            """,
        );
        ```
        Calling
        ```coffee
        <<< environments.get_definition('maths-block'); >>>
        ```
        displays
        ```tex
        \\providecommand{\\maths}{}
        \\renewenvironment{\\maths}[2]{%
            \\begin{math}\\relax%
            \\begin{array}[#2]{#1}\\relax%
        }{%
            \\end{array}\\relax%
            \\end{math}\\relax%
        }
        ```
        in .tex files, and
        ```coffee
        <<< macros.begin('maths-block', halign='rcl', valign='t'); >>>
            y &= &x\\\\
              &= &z\\\\
        <<< macros.end('maths-block'); >>>
        ```
        displays
        ```tex
        \\begin{maths}{rcl}{t}
            y &= &x\\\\
              &= &z\\\\
        \\end{maths}
        ```
        in .tex files.
        '''
        ## anonymise begin/end and create definition:
        begin, n_ = anonymise_arguments(contents=begin, n=n, keys=keys);
        end,   _  = anonymise_arguments(contents=end,   n=0, keys=[]);
        name = name if isinstance(name, str) else alias;
        definition = createEnvironmentDefinition(name=name, overwrite=overwrite, multiline=multiline, n=n_, begin=begin, end=end);
        usage_begin = createEnvironmentUsageBegin(name=name, n=n, keys=keys);
        usage_end = createEnvironmentUsageEnd(name=name);
        ## add new environment in dictionary:
        self._objects[alias] = LatexEnvironment(
            alias      = alias,
            anon       = False,
            overwrite  = overwrite,
            begin      = LatexMacro(alias=alias, anon=True, overwrite=False, usage=usage_begin),
            end        = LatexMacro(alias=alias, anon=True, overwrite=False, usage=usage_end),
            definition = definition,
        );
        return;

    # Intention: should creates explicit LaTeX definition. This can be customised.
    def add_anon(
        self,
        alias: str,
        begin: Callable[..., str],
        end:   Callable[..., str],
    ):
        '''
        ## Create anonymous LaTeX environment definition ##

        @inputs
        - `alias` - how command should be referred to in python.
        - `usage` - implicit method

        ## Example ##

        ```py
        environments = LatexEnvironments();
        environments.add_anon(alias='maths-block',
            begin = lambda valign, halign: \
                r"\\begin{{math}}\\begin{{array}}[{{v}}]{{{h}}}".format(v=valign, h=halign)
            end = lambda: r"\\end{array}\\end{math}"
        );
        ```
        Using
        ```coffee
        <<< environments.getDefinition('maths-block'); >>>
        ```
        displays an empty line in .tex files. And
        ```coffee
        <<< macros.begin('maths-block', halign='rcl', valign='t'); >>>
            y &= &x\\\\
              &= &z\\\\
        <<< macros.end('maths-block'); >>>
        ```
        displays:
        ```tex
        \\begin{math}\\begin{array}[t]{rcl}
            y &= &x\\\\
              &= &z\\\\
        \\end{array}\\end{math}
        ```
        in .tex files.
        '''
        self._objects[alias] = LatexEnvironment(alias=alias, anon=True, begin=begin, end=end);
        return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def createEnvironmentDefinition(
    name:      str,
    overwrite: bool,
    multiline: bool,
    n:         int,
    begin:     str,
    end:       str
) -> str:
    '''
    Creates native LaTeX environment definition.
    '''
    options = dict(
        name  = name,
        n     = n,
        begin = join_lines(clean_lines(begin), relax=True, percent=True),
        end   = join_lines(clean_lines(end), relax=True, percent=True),
        multi = '' if multiline else '*',
    );
    if overwrite:
        return dedentIgnoreFirstAndLast('''
            \\providecommand{{\\{name}}}{{}}
            \\renewenvironment{{\\{name}}}[{n}]{{{begin}}}{{{end}}}
        ''').format(**options);
    return dedentIgnoreFirstAndLast('''
        \\newenvironment{{\\{name}}}[{n}]{{{begin}}}{{{end}}}
    ''').format(**options);

def createEnvironmentUsageBegin(name: str, n: int, keys: List[str]) -> Callable[..., str]:
    '''
    Creates usage function for begin-method of explicitly defined LaTeX environment.
    '''
    def usage(*_, **__) -> str:
        args_string = convert_args_to_latex_args_as_string(n=n, keys=keys, args=_, kwargs=__);
        return '\\begin{{{name}}}{args}'.format(name=name, args=args_string);
    return usage;

def createEnvironmentUsageEnd(name: str) -> Callable[..., str]:
    '''
    Creates usage function for end-method of explicitly defined LaTeX environment.
    '''
    def usage(*_, **__) -> str:
        return '\\end{{{name}}}'.format(name=name);
    return usage;
