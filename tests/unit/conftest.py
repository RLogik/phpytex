#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from unittest import TestCase
from pytest import fixture

# ----------------------------------------------------------------
# FIXTURES
# ----------------------------------------------------------------


@fixture(scope='session')
def test():
    return TestCase()


@fixture(scope='session')
def debug():
    def log(*lines: str):
        with open('logs/debug.log', 'a') as fp:
            for line in lines:
                print(line, end='\n', file=fp)

    return log
