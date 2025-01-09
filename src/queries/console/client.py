#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from argparse import ArgumentParser

from ..._core.utils.basic import *
from ..._core.utils.misc import *
from ...models.application import *
from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "CliArguments",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


class CliArguments(CliArgumentsBase):
    _part = "CLI"

    def create_parser(self) -> ArgumentParser:
        parser = self.baseparser
        parser.add_argument(
            "mode",
            choices=[e.value for e in EnumProgrammeMode],
            type=EnumProgrammeMode,
            help=dedent(
                f"""
                {EnumProgrammeMode.VERSION.value} = show version of programme
                {EnumProgrammeMode.RUN.value} = run a feature
                """
            ),
        )
        parser.add_argument(
            "feature",
            nargs="?",
            choices=[e.value for e in EnumFeatures],
            type=EnumFeatures,
            help=dedent(
                f"""
                {EnumFeatures.TRANSPILE.value} = run the transpilation feature
                """
            ),
            default=None,
        )
        parser.add_argument(
            "--path",
            nargs="?",
            help="Path to user working directory",
            default=None,
        )
        parser.add_argument(
            "--config",
            nargs="?",
            type=str,
            help=dedent(
                f"""
                File name for user config within working directory.
                If empty, automatically searches for first file that matches:
                  {self._appconfig.user_config_pattern}
                """
            ),
        )
        parser.add_argument(
            "--parameters",
            type=parse_json_as_dict("--parameters"),
            nargs="?",
            help="JSON encoded object to override user config / parameter settings on-the-fly.",
            default=None,
        )
        parser.add_argument(
            "--compile",
            type=parse_json_as_dict("--compile"),
            nargs="?",
            help="JSON encoded object to override user config / compile settings on-the-fly.",
            default=None,
        )
        parser.add_argument(
            "--quiet",
            "-q",
            action="store_true",
            help="Make logging less verbose.",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Force logging level to be DEBUG.",
        )
        parser.add_argument(
            "--log",
            nargs="?",
            type=str,
            help="Path to files for logging.",
            default=None,
        )
        return parser
