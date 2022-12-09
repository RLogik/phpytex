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
from src.models.cli import *;

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
            description=dedent('''
            Phpytex
            ~~~~~~~
            A transpiler that converts

              python-augmented LaTeX ~~ into ~~> pure python ~~ into ~~> pure LaTeX.

            Example usage:

                phpytex example && phpytex run
            '''),
            formatter_class=argparse.RawTextHelpFormatter,
        );
        parser.add_argument('mode',
            nargs = '?',
            choices = ['version', 'help', 'run', 'transpile' 'template', 'example'],
            help = dedent('''
            - help:               Display this help.
            - version:            Display version.
            - run/transpile:      Run the phpytex transpiler.
            - template:           Generate a bare template for a phpytex config file.
            - example:            Generate an example template for a phpytex config file.
            '''),
        );
        parser.add_argument(
            '--quiet',
            action = 'store_true',
            default = False,
            help = 'Hide all but the most important console messages during transpilation.');
        parser.add_argument(
            '--debug',
            action = 'store_true',
            default = False,
            help = 'Display debugging (for development only).');
        parser.add_argument(
            '--plain',
            action = 'store_true',
            default = False,
            help = 'If set, console logging will be performed without special terminal fonts.');
        parser.add_argument(
            '--file', '--config',
            nargs = '?',
            type = str,
            help = '(string) Path to config file (default is .phytex.yaml).');
        parser.add_argument(
            '--parameters-options',
            '--parameters', # <- only need this for old versions
            nargs = '?',
            type = str,
            help = '(json) On-the-fly definition of paramaters (overrides parameters > options in user config file).');
        parser.add_argument(
            '--transpile-options',
            nargs = '?',
            type = str,
            help = '(json) On-the-fly definition of transpilation options (overrides transpile > options in user config file).');
        parser.add_argument(
            '--stamp-options',
            nargs = '?',
            type = str,
            help = '(json) On-the-fly definition of stamp options (overrides stamp > options in user config file).');
    return parser;
