#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
from textwrap import dedent;
from typing import Any;
from typing import Dict;
from typing import List;
from typing import Tuple;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'dedentIgnoreFirstAndLast',
    'clean_lines',
    'join_lines',
    'anonymise_arguments',
    'convert_args_to_latex_args',
    'convert_args_to_latex_args_as_string',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS - STRINGS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dedentIgnoreFirstAndLast(s: str) -> str:
    s = re.sub(r'^\s*\r?\n|\r?\n\s*$', '', s);
    return dedent(s);

def clean_lines(contents: str) -> List[str]:
    lines = re.split(r'\r?\n', dedent(contents));
    while len(lines) > 0 and lines[0] == '':
        lines = lines[1:];
    while len(lines) > 0 and lines[-1] == '':
        lines = lines[:-1];
    return lines;

def join_lines(lines: List[str], relax=False, percent=False) -> str:
    if len(lines) <= 1:
        return ''.join(lines);
    eol = '{relax}{percent}'.format(
        relax = r'\relax' if relax else '',
        percent = r'%' if percent else '',
    );
    indent = r'    ';
    return ('%' + '\n' + indent) + (eol + '\n' + indent).join(lines) + (eol + '\n');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS - CONVERSION OF ARGUMENTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def anonymise_arguments(
    contents: str,
    n: int,
    keys: List[str]
) -> Tuple[str, int]:
    '''
    ## Anonymise LaTeX definition ##

    @inputs
    - `contents` - LaTeX string
    - `n` - number of anonymous arguments (viewed as arguments #1, #2, ..., #n)
    - `keys` - ordered list of of named arguments

    @returns
    - `contents` as new string with named arguments replaced by #(n+1), ...
    - `n` - new number of arguments in command
    '''
    ## replace all whole word occurrences of each key by #<index>:
    for index, key in enumerate(keys):
        pattern = r'\b{}\b'.format(key);
        repl = '#{}'.format(n + (index + 1));
        contents = re.sub(pattern, repl, string=contents);
    n += len(keys);
    return contents, n;

def convert_args_to_latex_args(n: int, keys: List[str], args: list, kwargs: Dict[str, Any]) -> List[Any]:
    '''
    Converts args + key-value args to anyonymised list to fit scheme of a command.

    @returns
    List of form `[arg1, arg2, ...]`.
    '''
    # force number of anon-arguments to be n:
    anonymised = (list(args) + ['' for _ in range(n)])[:n];
    # add in kwargs as anonymised ordered list based on keys:
    anonymised += [ kwargs[key] if key in kwargs else '' for key in keys ];
    return anonymised;

def convert_args_to_latex_args_as_string(n: int, keys: List[str], args: list, kwargs: Dict[str, Any]) -> List[Any]:
    '''
    Converts args + key-value args to anyonymised list to fit scheme of a command.

    @returns
    String of form `{arg1}{arg2}...`.
    '''
    anonymised = convert_args_to_latex_args(n=n, keys=keys, args=args, kwargs=kwargs);
    return ''.join([ '{{{}}}'.format(arg) for arg in anonymised ]);
