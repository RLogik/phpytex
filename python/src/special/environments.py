#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from copy import copy;
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
    _alias: str;
    _anon: bool;
    _overwrite: bool;
    _definition: str;
    _command: str;
    _begin: LatexMacro;
    _end: LatexMacro;
    _got: bool;

    def __init__(
        self,
        alias:      str,
        anon:       bool,
        begin:      LatexMacro,
        end:        LatexMacro,
        definition: str  = '',
        overwrite:  bool = False,
        command:    str = '',
    ):
        self._alias = alias;
        self._anon = anon;
        self._overwrite = overwrite;
        self._definition = definition;
        self._begin = begin;
        self._end = end;
        self._command = command;
        self._got = False;
        return;

    @property
    def alias(self) -> str:
        return self._alias;

    @property
    def anon(self) -> bool:
        return self._anon;

    @property
    def overwrite(self) -> bool:
        return self._overwrite;

    @property
    def definition(self) -> str:
        self._got = True;
        return '' if self._anon else self._definition;

    @property
    def command(self) -> str:
        return self._command;

    @property
    def begin(self) -> LatexMacro:
        return self._begin;

    @property
    def end(self) ->   LatexMacro:
        return self._end;

    def __copy__(self):
        e = LatexEnvironment(
            alias      = self._alias,
            anon       = self._anon,
            overwrite  = self._overwrite,
            definition = self._definition,
            begin      = copy(self._begin),
            end        = copy(self._end),
            command    = self._command,
        );
        e._got = self._got;
        return e;

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

    def command(self, alias: str) -> str:
        e = self.get(alias);
        if e.anon:
            raise Exception('LATEX environment \033[1m{}\033[0m is anonymous, thus has no native counterpart.'.format(alias));
        return e.command;

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
    ) -> LatexEnvironment:
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

        @returns
        - `e` - the added LaTeX environment

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
            command    = '\\{}'.format(name),
            definition = definition,
        );
        return self._objects[alias];

    # Intention: should creates explicit LaTeX definition. This can be customised.
    def add_anon(
        self,
        alias: str,
        begin: Callable[..., str],
        end:   Callable[..., str],
    ) -> LatexEnvironment:
        '''
        ## Create anonymous LaTeX environment definition ##

        @inputs
        - `alias` - how command should be referred to in python.
        - `usage` - implicit method

        @returns
        - `e` - the added LaTeX environment

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
        return self._objects[alias];

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
