#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from math import isnan
from math import nan

from safetywrap import Err
from safetywrap import Ok
from safetywrap import Result

from tests.unit.thirdparty.unit import *

from src._core.utils.code import *

# ----------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------


def test_CoerceType_INT(
    test: TestCase,
):
    coerce = TypeGuard[int, None](type=int)
    test.assertEqual(coerce(5), 5)
    test.assertIsNone(coerce(5.0))
    test.assertIsNone(coerce("cat"))

    coerce = TypeGuard[int, int](type=int, default=-1)
    test.assertEqual(coerce(5), 5)
    test.assertEqual(coerce(5.0), -1)
    test.assertEqual(coerce("cat"), -1)

    coerce = TypeGuard[int, int](type=int, default_factory=len)
    test.assertEqual(coerce(5), 5)
    test.assertEqual(coerce("cat"), 3)


def test_CoerceType_FLOAT(
    test: TestCase,
):
    coerce = TypeGuard[float, None](type=float)
    test.assertEqual(coerce(5.0), 5.0)
    test.assertIsNone(coerce(5))
    test.assertIsNone(coerce("cat"))

    coerce = TypeGuard[float, float](type=float, default=nan)
    test.assertEqual(coerce(5.0), 5.0)
    test.assertTrue(coerce(5))
    test.assertTrue(isnan(coerce("cat")))

    coerce = TypeGuard[float, float](type=float, default_factory=float)
    test.assertEqual(coerce(5.0), 5.0)
    test.assertEqual(coerce(5), 5.0)
    test.assertEqual(coerce("5"), 5.0)

    coerce = TypeGuard[float, str](type=float, default_factory=str)
    test.assertEqual(coerce(5.0), 5.0)
    test.assertEqual(coerce(5), "5")
    test.assertEqual(coerce("5"), "5")


def test_CoerceType_BOOLEAN(
    test: TestCase,
):
    coerce = TypeGuard[bool, None](type=bool)
    test.assertEqual(coerce(True), True)
    test.assertEqual(coerce(False), False)
    test.assertIsNone(coerce("True"))
    test.assertIsNone(coerce("true"))
    test.assertIsNone(coerce("False"))
    test.assertIsNone(coerce("false"))
    test.assertIsNone(coerce(0))
    test.assertIsNone(coerce(1))
    test.assertIsNone(coerce(5))
    test.assertIsNone(coerce("cat"))

    coerce = TypeGuard[bool, float](type=bool, default=nan)
    test.assertEqual(coerce(True), True)
    test.assertEqual(coerce(False), False)
    test.assertTrue(isnan(coerce("True")))
    test.assertTrue(isnan(coerce("true")))
    test.assertTrue(isnan(coerce("False")))
    test.assertTrue(isnan(coerce("false")))
    test.assertTrue(isnan(coerce(5)))
    test.assertTrue(isnan(coerce("cat")))


def test_wrap_result_SIMPLE(
    test: TestCase,
):
    @wrap_result
    def my_method(x: int, /) -> float:
        if 0 <= x and x < 10:
            return 0.1 * x

        else:
            raise ValueError(f"expected a value between 0 (incl.) and 1 (excl.) but received {x}")  # fmt: skip

    with assert_not_raises():
        result = my_method(4)
        test.assertIsInstance(result, Ok)
        value = result.unwrap()
        test.assertAlmostEqual(value, 0.4)

        result = my_method(12)
        test.assertIsInstance(result, Err)
        err = result.unwrap_err()
        test.assertIsInstance(err, ValueError)
        test.assertEqual(str(err), "expected a value between 0 (incl.) and 1 (excl.) but received 12")  # fmt: skip
    return


def test_wrap_result_NESTED(
    test: TestCase,
):
    @wrap_result
    def my_method(x: int, /) -> Result[float, ValueError]:
        if 0 <= x and x < 10:
            return Ok(0.1 * x)

        else:
            return Err(ValueError(f"expected a value between 0 (incl.) and 1 (excl.) but received {x}"))  # fmt: skip

    with assert_not_raises():
        result = my_method(4)
        test.assertIsInstance(result, Ok)
        value = result.unwrap()
        test.assertAlmostEqual(value, 0.4)

        result = my_method(6)
        test.assertIsInstance(result, Ok)
        value = result.unwrap()
        test.assertAlmostEqual(value, 0.6)

        result = my_method(12)
        test.assertIsInstance(result, Err)
        err = result.unwrap_err()
        test.assertIsInstance(err, ValueError)
        test.assertEqual(str(err), "expected a value between 0 (incl.) and 1 (excl.) but received 12")  # fmt: skip

        result = my_method(23)
        test.assertIsInstance(result, Err)
        err = result.unwrap_err()
        test.assertIsInstance(err, ValueError)
        test.assertEqual(str(err), "expected a value between 0 (incl.) and 1 (excl.) but received 23")  # fmt: skip
    return
