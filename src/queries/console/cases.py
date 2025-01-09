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
    _part = "TEST CASES"

    def create_parser(self) -> ArgumentParser:
        parser = self.baseparser
        parser.add_argument(
            "mode",
            choices=[e.value for e in EnumProgrammeMode],
            type=EnumProgrammeMode,
            help=dedent(
                f"""
                {EnumProgrammeMode.VERSION.value} = show version of programme
                {EnumProgrammeMode.RUN.value} = run programme
                """
            ),
        )
        add_boolean_key_pair(
            parser=parser,
            key="inspect",
            default=False,
            help_true="Run test cases with inspection",
            help_false="Run test cases without inspection",
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
