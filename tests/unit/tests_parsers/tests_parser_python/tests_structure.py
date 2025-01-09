#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from tests.unit.thirdparty.fake import *
from tests.unit.thirdparty.unit import *

from src._core.utils.misc import *
from src.parsers.parser_python.structure import *

# ----------------------------------------------------------------
# FIXTURES
# ----------------------------------------------------------------

#

# ----------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------


@mark.parametrize(
    ("text", "n_expected"),
    [
        (
            dedent(
                """
                x = 5
                """
            ),
            0,
        ),
        (
            dedent(
                """
                        x = 5
                y = 1
                """
            ),
            2,
        ),
        (
            dedent(
                """
                        # some comment
                        x = 5
                y = 1
                """
            ),
            2,
        ),
    ],
)
def test_get_size_of_first_indentation_CASES(
    # fixtures
    test: TestCase,
    # parameters
    text: str,
    n_expected: int,
):
    n = get_size_of_first_indentation(text, indent="    ")
    test.assertEqual(n, n_expected)
    return


@mark.parametrize(
    ("text", "n_expected"),
    [
        ("", 0),
    ],
)
def test_get_size_of_first_indentation_EDGE_CASES(
    # fixtures
    test: TestCase,
    # parameters
    text: str,
    n_expected: int,
):
    n = get_size_of_first_indentation(text, indent="    ")
    test.assertEqual(n, n_expected)
    return


def test_get_size_of_first_indentation_FIXTURES(
    # fixtures
    test: TestCase,
    codelines0a: str,
    codelines1a: str,
    # parameters
):
    text = codelines0a
    n = get_size_of_first_indentation(text, indent="    ")
    test.assertEqual(n, 0)

    text = codelines1a
    n = get_size_of_first_indentation(text, indent="    ")
    test.assertEqual(n, 1)
    return


def test_get_sizes_of_final_indentations_FIXTURES(
    # fixtures
    test: TestCase,
    codelines0a: str,
    codelines0b: str,
    codelines0c: str,
    codelines1a: str,
    codelines1b: str,
    codelines2a: str,
    codelines2b: str,
    # parameters
):
    text = codelines0a
    indents = get_sizes_of_final_indentations(text, indent="    ")
    test.assertEqual(len(indents), 1)
    test.assertListEqual(indents, [1])

    text = codelines0b
    indents = get_sizes_of_final_indentations(text, indent="    ")
    test.assertEqual(len(indents), 1)
    test.assertListEqual(indents, [2])

    text = codelines0c
    indents = get_sizes_of_final_indentations(text, indent="    ")
    test.assertEqual(len(indents), 1)
    test.assertListEqual(indents, [3])

    text = codelines1a
    indents = get_sizes_of_final_indentations(text, indent="    ")
    test.assertEqual(len(indents), 2)
    test.assertListEqual(indents, [1, 2])

    text = codelines1b
    indents = get_sizes_of_final_indentations(text, indent="    ")
    test.assertEqual(len(indents), 2)
    test.assertListEqual(indents, [2, 3])

    text = codelines2a
    indents = get_sizes_of_final_indentations(text, indent="    ")
    test.assertEqual(len(indents), 3)
    test.assertListEqual(indents, [2, 3, 4])

    text = codelines2b
    indents = get_sizes_of_final_indentations(text, indent="    ")
    test.assertEqual(len(indents), 3)
    test.assertListEqual(indents, [2, 3, 4])
    return


def test_get_size_of_final_indentation_FIXTURES(
    # fixtures
    test: TestCase,
    codelines0a: str,
    codelines0b: str,
    codelines0c: str,
    codelines1a: str,
    codelines1b: str,
    codelines2a: str,
    codelines2b: str,
    # parameters
):
    text = codelines0a
    level = get_size_of_final_indentation(text, indent="    ")
    test.assertEqual(level, 1)

    text = codelines0b
    level = get_size_of_final_indentation(text, indent="    ")
    test.assertEqual(level, 2)

    text = codelines0c
    level = get_size_of_final_indentation(text, indent="    ")
    test.assertEqual(level, 3)

    text = codelines1a
    level = get_size_of_final_indentation(text, indent="    ")
    test.assertEqual(level, 2)

    text = codelines1b
    level = get_size_of_final_indentation(text, indent="    ")
    test.assertEqual(level, 3)

    text = codelines2a
    level = get_size_of_final_indentation(text, indent="    ")
    test.assertEqual(level, 4)

    text = codelines2b
    level = get_size_of_final_indentation(text, indent="    ")
    test.assertEqual(level, 4)
    return
