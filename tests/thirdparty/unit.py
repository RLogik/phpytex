#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# for unit tests:
from contextlib import nullcontext as does_not_raise;
from pytest import fixture;
from pytest_lazyfixture import lazy_fixture;
from pytest import LogCaptureFixture;
from pytest import mark;
from pytest import raises as assert_raises;
from testfixtures import LogCapture;
from unittest import TestCase;
from unittest.mock import patch;
from unittest.mock import MagicMock;
from unittest.mock import PropertyMock;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'assert_raises',
    'does_not_raise',
    'fixture',
    'lazy_fixture',
    'LogCapture',
    'LogCaptureFixture',
    'MagicMock',
    'mark',
    'patch',
    'PropertyMock',
    'TestCase',
];
