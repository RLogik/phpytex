#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pytest;
from pytest import mark;
from pytest import fixture;
from pytest import lazy_fixture;
from unittest import TestCase;
from unittest.mock import MagicMock;
from unittest.mock import patch;

from src.local.typing import *;
from src.graphs.graph import *;
from src.graphs.tarjan import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIXTURES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# @fixture(scope='module')
# def ...

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test Tarjan-Algorithm
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@mark.usefixtures('test')
def test_isLinux(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_PythonCommand(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_pipeCall(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_getFullPath(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_formatPath(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_getFiles(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_getFilesByPattern(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_createNewPathName(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_createNewFileName(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_createPath(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_createFile(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_readTextFile(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_writeTextFile(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_getCliArgs(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_escapeForPython(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_dedentIgnoreEmptyLines(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_dedentRelativeTo(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_dedentIgnoreFirstAndLast(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_formatBlockUnindent(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_formatBlockIndent(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_formatTextBlock(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_formatTextBlockAsList(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_extractIndent(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_lengthOfWhiteSpace(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_sizeOfIndent(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_unique(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_inheritanceOnGraph(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_readYamlFile(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_restrictDictionary(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_toPythonKeys(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_toPythonKeysDict(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_getAttributeIgnoreError(test):
    test.assertEqual('', '');

@mark.usefixtures('test')
def test_getAttribute(test):
    test.assertEqual('', '');
