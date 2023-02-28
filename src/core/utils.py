#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'escape_for_python',
    'extract_indent',
    'flatten',
    'is_linux',
    'length_of_white_space',
    'pipe_call',
    'python_command_split',
    'python_command',
    'size_of_indent',
    'text_block_indent',
    'text_block_unindent',
    'unique',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOCAL VARIABLES / CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

T = TypeVar('T');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD - system
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def is_linux() -> bool:
    # return not ( os.name == 'nt' );
    return not ( platform.system().lower() == 'windows' );

def python_command_split() -> list[str]:
    return [ 'python3' ] if is_linux() else ['py', '-3'];

def python_command() -> str:
    return ' '.join(python_command_split());

def pipe_call(
    *args: str,
    cwd: Optional[str] = None,
    error_msg: Optional[str] = None,
    fname_out: Optional[str] = None
) -> None:
    '''
    Executes a command as a subprocess and waits for result.

    NOTE: subprocess.run is like subprocess.Popen but waits for result
    '''
    cwd = cwd or os.getcwd();
    if fname_out is None:
        result = subprocess.run(list(args), cwd=cwd)
    else:
        with open(fname_out, 'w') as fp:
            result = subprocess.run(list(args), cwd=cwd, stdout=fp);
    if result.returncode == 0:
        return;
    raise Exception(error_msg or f'Shell command {{{ " ".join(args) }}} failed.');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: strings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# escapes string for use in python code
def escape_for_python(s: str, with_formatting: bool = False) -> str:
    s = re.sub(r'(\\+)', r'\1\1', s);
    s = re.sub(r'\n', r'\\n', s);
    s = re.sub(r'\t', r'\\t', s);
    s = re.sub(r'\"', r'\\u0022', s);
    s = re.sub(r'\'', r'\\u0027', s);
    # s = re.sub(r'\%', slash+'u0025', s);
    if with_formatting:
        s = re.sub(r'(\{+)', r'\1\1', s);
        s = re.sub(r'(\}+)', r'\1\1', s);
    return s;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: string - remove and set indentation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def text_block_unindent(lines: list[str], reference: str) -> list[str]:
    s = dedent('\n'.join([ reference + '.' ] + lines));
    return s.split('\n')[1:];

def text_block_indent(lines: list[str], indent: str, unindent: bool = True) -> list[str]:
    if unindent:
        s = dedent('\n'.join(lines));
        lines = s.split('\n');
    return [ indent + line for line in lines ];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: string - compute white spaces and indents
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def extract_indent(s: str) -> str:
    return re.sub(r'^(\s*).*$', r'\1', s);

def length_of_white_space(text: str) -> int:
    '''
    Computes the white space length of a string.
    Ignores all characters except `' '` and `'\\t'`.
    '''
    n = 0;
    for u in text:
        match u:
            # add 1 for spaces
            case ' ':
                n += 1;
            # 'go to' next tab stop in case of tab
            case '\t':
                n = (n - n % 8) + 8;
    return n;

def size_of_indent(space: str, unit: str) -> tuple[int, int]:
    '''
    Computes the size of white space relative to a given indent symbol.

    @inputs
    - `s` - white space string
    - `indent_symbol` - white space string used as a base reference.

    @returns
    `(n, r)` where `n` = number of instance of base unit
    and `r` = remainder white space in absolute terms (relative to single spaces).
    '''
    len_space = length_of_white_space(space);
    len_unit = length_of_white_space(unit);
    n = int(len_space / len_unit);
    r = len_space - n * len_unit;
    return (n, r);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: array methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def unique(X: list[T]) -> list[T]:
    X_ = [];
    for el in X:
        if el in X_:
            continue;
        X_.append(el);
    return X_;

def flatten(XX: list[list[T]]) -> list[T]:
    X = [];
    for X_ in XX:
        X += X_;
    return X;
