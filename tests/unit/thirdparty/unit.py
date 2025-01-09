#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from contextlib import nullcontext as assert_not_raises
from itertools import product as itertools_product
from unittest import TestCase
from unittest import skip
from unittest import skipIf
from unittest import skipUnless
from unittest.mock import MagicMock
from unittest.mock import PropertyMock
from unittest.mock import patch

from pytest import LogCaptureFixture
from pytest import fixture
from pytest import mark
from pytest import raises as assert_raises
from testfixtures import LogCapture

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "LogCapture",
    "LogCaptureFixture",
    "MagicMock",
    "PropertyMock",
    "TestCase",
    "assert_not_raises",
    "assert_raises",
    "fixture",
    "itertools_product",
    "mark",
    "patch",
    "skip",
    "skipIf",
    "skipUnless",
]
