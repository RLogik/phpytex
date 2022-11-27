#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.io import *;
from src.thirdparty.misc import *;
from src.thirdparty.types import *;

from src.core.log import *;
from src.core.utils import *;
from src.models.internal import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'display_help',
    'display_usage',
    'get_arguments_from_cli',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS/VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

parser = None;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_arguments_from_cli(*cli_args: str) -> ProgrammeArguments:
    '''
    Extracts CLI arguments.
    '''
    try:
        parser = get_argument_parser();
        args = vars(parser.parse_args(cli_args));
        return ProgrammeArguments(**{
            key: value
            for key, value in args.items()
            if value is not None
        });
    except Exception as e:
        display_usage();
        exit(1);

def display_help() -> None:
    '''
    Displays the usages of programme with CLI arguments.
    '''
    parser = get_argument_parser();
    parser.print_help();
    return;

def display_usage() -> None:
    '''
    Displays the full help file for CLI arguments for programme.
    '''
    parser = get_argument_parser();
    parser.print_usage();
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_argument_parser() -> argparse.ArgumentParser:
    '''
    Constructs parser for CLI-arguments, if not already defined.
    '''
    global parser;
    if not isinstance(parser, argparse.ArgumentParser):
        parser = argparse.ArgumentParser(
            prog='code/main.py',
            description=dedent('''
            Phpytex:
            A transpiler that converts python augmented LaTeX into pure python then pure LaTeX.
            '''),
            formatter_class=argparse.RawTextHelpFormatter,
        );
        parser.add_argument('mode',
            nargs='?',
            choices=['version', 'help', 'run'],
            help=dedent('''
            - help:     Display this help.
            - version:  Display version.
            - run:      Run the Phpytex transpiler.
            '''),
        );
        parser.add_argument('--quiet', action='store_true', default=False, help='Hide all but the most important console messages during transpilation.');
        parser.add_argument('--debug', action='store_true', default=False, help='Display debugging (for development only).');
        parser.add_argument('--colour', action='store_true', default=True, help='(Under construction) Whether to display messages with special terminal fonts.');
        parser.add_argument('--file',   nargs='?', type=str, help='(string) Path to config file (default is .phytex.yaml).');
        parser.add_argument('--parameters',   nargs='?', type=str, help='(json) On-the-fly definition of paramaters to override parameters > options from config file.');
    return parser;
