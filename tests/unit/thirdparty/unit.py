#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import anyio
from contextlib import nullcontext as does_not_raise
from itertools import product as itertools_product
from pytest import fixture
from pytest_lazyfixture import lazy_fixture
from pytest import LogCaptureFixture
from pytest import mark
from pytest import raises as assert_raises
from testfixtures import LogCapture
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import PropertyMock

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'LogCapture',
    'LogCaptureFixture',
    'MagicMock',
    'PropertyMock',
    'TestCase',
    'anyio',
    'assert_raises',
    'does_not_raise',
    'fixture',
    'itertools_product',
    'lazy_fixture',
    'mark',
    'patch',
]
