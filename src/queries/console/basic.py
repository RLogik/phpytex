#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import json
import re
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

from ..._core.utils.misc import *
from ...models.internal import *
from ...setup import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "CliArgumentsBase",
    "add_boolean_key_pair",
    "parse_json_as_dict",
]

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class CliArgumentsBase:
    _parser = None
    _info: RepoInfo
    _appconfig: AppConfig
    _prog: str = "main.py"
    _part: str | None = None

    def __init__(self, info: RepoInfo, appconfig: AppConfig):
        self._info = info
        self._appconfig = appconfig

    def parse(self, *cli_args: str):
        return self.parser.parse_args(cli_args)

    @property
    def parser(self) -> ArgumentParser:
        if not isinstance(self._parser, ArgumentParser):
            self._parser = self.create_parser()
        return self._parser

    @property
    def baseparser(self) -> ArgumentParser:
        description = re.sub(pattern=r"(\r?\n)+", repl=" ", string=self._info.description)
        part = "" if self._part is None else f" - {self._part}"
        parser = ArgumentParser(
            prog=self._prog,
            description=dedent(
                f"""
                \x1b[1mProgramme: {self._info.name} @ v{self._info.version}{part}\x1b[0m
                \x1b[2murl: \x1b[4m{self._info.urls.homepage}\x1b[0m
                \x1b[2;3m{description}\x1b[0m
                """
            ),
            formatter_class=RawTextHelpFormatter,
        )
        return parser

    def create_parser(self) -> ArgumentParser:
        parser = self.baseparser
        return parser


# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def add_boolean_key_pair(
    parser: ArgumentParser,
    key: str,
    default: bool,
    help_true: str | None = None,
    help_false: str | None = None,
):
    """
    Adds a pair of boolean switches to the argparser
    """
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(f"--{key}", dest=key, action="store_true", help=help_true)
    group.add_argument(f"--no-{key}", dest=key, action="store_false", help=help_false)
    parser.set_defaults(**{key: default})
    return parser


def parse_json_as_dict(name: str):
    """
    Creates a JSON -> dict parser for a flag.
    """

    def parser(text: str) -> dict:
        result = json.loads(text)
        assert isinstance(
            result, dict
        ), f"{name} expects a JSON-encoded dictionary. Received {text}."
        return result

    return parser
