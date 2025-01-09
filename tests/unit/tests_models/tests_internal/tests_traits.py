#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from tests.unit.thirdparty.fake import *
from tests.unit.thirdparty.unit import *

from src.models.internal.traits import *

# ----------------------------------------------------------------
# FIXTURES
# ----------------------------------------------------------------

#

# ----------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------


def test_class_properties_BASIC1(
    test: TestCase,
):
    temperature = Property[float]()
    temperature.set(273.15)
    value = temperature()
    test.assertEqual(value, 273.15)
    return


def test_class_properties_BASIC2(
    test: TestCase,
):
    name = Property[str]()
    with test.assertRaises(Exception, msg="value should not yet exist"):
        value = name()
    name.set("Julia")
    test.assertEqual(name(), "Julia")
    return


def test_class_properties_FINAL1(
    test: TestCase,
):
    temperature = FinalProperty[float]()
    temperature.set(100.0)
    with test.assertRaises(Exception, msg="should not be able to override final value"):
        temperature.set(0.1)
    test.assertEqual(temperature(), 100.0)
    return


def test_class_properties_FINAL3(
    test: TestCase,
):
    temperature = Property[float]()
    temperature.set(100.0)
    temperature.set(0.1)
    test.assertEqual(temperature(), 0.1)
    return


def test_class_properties_FACTORY(
    test: TestCase,
):
    mock = MagicMock(return_value="Max Mustermann")
    mock.assert_not_called()

    name = Property[str](mock)
    mock.assert_not_called()

    test.assertEqual(name(), "Max Mustermann")
    mock.assert_called_once()
    test.assertEqual(mock.call_count, 1)

    test.assertEqual(name(), "Max Mustermann", "factory should be called")
    test.assertEqual(mock.call_count, 1, "Computation of value should be performed once!")
    return


def test_class_properties_FACTORY_PRECENDENCE_FACTORY(
    test: TestCase,
):
    name = FinalProperty[str](lambda: "Max Mustermann")
    test.assertEqual(name(), "Max Mustermann", "factory should be called")
    with test.assertRaises(
        Exception, msg="sinc factory has been called, should not be able to override value"
    ):
        name.set("Julia Musterfrau")
    return


def test_class_properties_FACTORY_PRECENDENCE_SET(
    test: TestCase,
):
    name = Property[str](lambda: "Max Mustermann")
    name.set("Julia Musterfrau")
    test.assertEqual(name(), "Julia Musterfrau", ".set(...) should take precedence")
    return


def test_class_triggerproperty_BASIC(
    test: TestCase,
):
    has_error = TriggerProperty()
    test.assertFalse(has_error.value)
    has_error.set()
    test.assertTrue(has_error.value, "should become true after trigger")
    has_error.set()
    test.assertTrue(has_error.value, "should remain true upon 2nd trigger")
    has_error.set()
    test.assertTrue(has_error.value, "should remain true upon multiple triggers")
    return
