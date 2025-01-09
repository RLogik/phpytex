#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from tests.unit.thirdparty.unit import *

from src._core.utils.basic import *

# ----------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------


@mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        (" ", 1),
        ("  ", 2),
        ("   ", 3),
        ("\t", 8),
        ("\t\t", 16),
        ("\t\t\t", 24),
    ],
)
def test_len_whitespace_BASIC_CASES(
    test: TestCase,
    # parameters
    text: str,
    expected: int,
):
    n = len_whitespace(text)
    test.assertEqual(n, expected)


@mark.parametrize(
    ("text", "expected"),
    [
        (" \t", 8),
        ("  \t", 8),
        ("\t   ", 11),
        (" \t   ", 11),
        ("  \t   ", 11),
        (" " * 7 + "\t", 8),
        (" " * 8 + "\t", 16),
        (" " * 9 + "\t", 16),
        (" " * 7 + "\t ", 9),
        (" " * 8 + "\t ", 17),
        (" " * 9 + "\t ", 17),
    ],
)
def test_len_whitespace_MIXED_CASES(
    test: TestCase,
    # parameters
    text: str,
    expected: int,
):
    n = len_whitespace(text)
    test.assertEqual(n, expected)


@mark.parametrize(
    ("text", "expected"),
    [
        (" some words", 1),
        ("  some words", 2),
        ("  \tsome words", 8),
        ("  \t \tsome words", 16),
        ("  \t \t  some words", 18),
        ("  \t \t  some words with spaces after   ", 18),
        ("  \t \t  some words with spaces after   \t ", 18),
    ],
)
def test_len_whitespace_PREDENT(
    test: TestCase,
    # parameters
    text: str,
    expected: int,
):
    n = len_whitespace(text, mode=-1)
    test.assertEqual(n, expected)


@mark.parametrize(
    ("text", "expected"),
    [
        ("some words ", 1),
        ("some words  ", 2),
        ("some words  \t", 8),
        ("some words  \t \t", 16),
        ("some words  \t \t  ", 18),
        ("   some words with spaces before  \t \t  ", 18),
        ("   \t some words with spaces before  \t \t  ", 18),
    ],
)
def test_len_whitespace_POSTDENT(
    test: TestCase,
    # parameters
    text: str,
    expected: int,
):
    n = len_whitespace(text, mode=1)
    test.assertEqual(n, expected)


@mark.parametrize(
    ("indent", "symb", "expected"),
    [
        ("", " ", 0),
        (" ", " ", 1),
        ("  ", " ", 2),
        ("   ", " ", 3),
        ("    ", " ", 4),
        ("", "  ", 0),
        ("  ", "  ", 1),
        ("    ", "  ", 2),
        ("      ", "  ", 3),
        ("        ", "  ", 4),
        ("", "    ", 0),
        ("    ", "    ", 1),
        ("        ", "    ", 2),
        ("              ", "    ", 3),
        ("                ", "    ", 4),
        ("", "\t", 0),
        ("\t", "\t", 1),
        ("\t\t", "\t", 2),
        ("\t\t\t", "\t", 3),
        ("\t\t\t\t", "\t", 4),
    ],
)
def test_size_of_whitespace_BASIC_CASES(
    test: TestCase,
    # parameters
    indent: str,
    symb: str,
    expected: int,
):
    n = size_of_whitespace(indent, symb)
    test.assertEqual(n, expected)


@mark.parametrize(
    ("indent", "symb", "expected"),
    [
        ("\t", " ", 8),
        (" \t", " ", 8),
        ("  \t", " ", 8),
        ("  \t ", " ", 9),
        ("  \t  ", " ", 10),
        ("\t", "  ", 4),
        (" \t", "  ", 4),
        ("  \t", "  ", 4),
        ("  \t ", "  ", 4),
        ("  \t  ", "  ", 5),
        ("\t", "    ", 2),
        (" \t", "    ", 2),
        ("  \t", "    ", 2),
        ("  \t ", "    ", 2),
        ("  \t    ", "    ", 3),
        ("  \t     ", "    ", 3),
        (" ", "\t", 0),
        ("  ", "\t", 0),
        ("   ", "\t", 0),
        (" " * 7, "\t", 0),
        (" " * 8, "\t", 1),
        ("\t \t", "\t", 2),
        ("\t \t   ", "\t", 2),
    ],
)
def test_size_of_whitespace_IMPERFECTIONS(
    test: TestCase,
    # parameters
    indent: str,
    symb: str,
    expected: int,
):
    n = size_of_whitespace(indent, symb)
    test.assertEqual(n, expected)
