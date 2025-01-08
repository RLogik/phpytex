#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from tests.unit.thirdparty.fake import *
from tests.unit.thirdparty.unit import *

from src._core.utils.misc import *
from src.models.internal.trees import *

# ----------------------------------------------------------------
# FIXTURES
# ----------------------------------------------------------------


class Node(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    name: str
    value: int | None = Field(default=None)

    def __str__(self):
        value = "-" if self.value is None else self.value
        return f"{self.name}: {value}"


@fixture(scope="function", autouse=False)
def example_trivial1() -> GenericTree[Node]:
    return GenericTree[Node].model_validate(
        {
            "root": {
                "name": "Alice",
            },
        }
    )


@fixture(scope="function", autouse=False)
def example_trivial2() -> GenericTree[Node]:
    return GenericTree[Node].model_validate(
        {
            "root": {
                "name": "Alice",
                "value": 100,
            },
        }
    )


@fixture(scope="function", autouse=False)
def example_non_trivial1() -> GenericTree[Node]:
    return GenericTree[Node].model_validate(
        {
            "root": {
                "name": "Alice",
                "value": 100,
            },
            "children": [
                {
                    "name": "Bob",
                    "value": 3,
                },
                {
                    "root": {
                        "name": "Charlie",
                        "value": 5,
                    },
                    "children": [
                        {
                            "name": "Charlie.A",
                            "value": 1,
                        },
                        {
                            "name": "Charlie.B",
                        },
                        {
                            "name": "Charlie.C",
                            "value": 2,
                        },
                    ],
                },
                {
                    "name": "Daniel",
                    "value": 2,
                },
            ],
        }
    )


@fixture(scope="function", autouse=False)
def example_non_trivial2() -> GenericTree[Node]:
    return GenericTree[Node].model_validate(
        {
            "root": {
                "name": "Alice",
                "value": 100,
            },
            "children": [
                {
                    "name": "Bob",
                    "value": 3,
                },
                {
                    "root": {
                        "name": "Charlie",
                        "value": 5,
                    },
                    "children": [
                        {
                            "name": "Charlie.A",
                            "value": 1,
                        },
                        {
                            "name": "Charlie.B",
                        },
                        {
                            "root": {
                                "name": "Charlie.C",
                                "value": 2,
                            },
                            "children": [
                                {
                                    "name": "Echo",
                                    "value": 7,
                                },
                                {
                                    "name": "Foxtrot",
                                    "value": -5,
                                },
                            ],
                        },
                    ],
                },
                {
                    "name": "Daniel",
                    "value": 2,
                },
            ],
        }
    )


# ----------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------


def test_class_GenericTree_print(
    test: TestCase,
    example_trivial1: GenericTree[Node],
    example_trivial2: GenericTree[Node],
    example_non_trivial1: GenericTree[Node],
    example_non_trivial2: GenericTree[Node],
):
    T = example_trivial1
    test.assertEqual(
        str(T),
        dedent(
            """
            Alice: -
            """
        ),  # fmt: skip
    )
    T = example_trivial2
    test.assertEqual(
        str(T),
        dedent(
            """
            Alice: 100
            """
        ),  # fmt: skip
    )
    T = example_non_trivial1
    test.assertEqual(
        str(T),
        dedent(
            """
            Alice: 100
            ├──  Bob: 3
            ├──  Charlie: 5
            │  ├──  Charlie.A: 1
            │  ├──  Charlie.B: -
            │  └──  Charlie.C: 2
            └──  Daniel: 2
            """
        ),  # fmt: skip
    )
    T = example_non_trivial2
    test.assertEqual(
        str(T),
        dedent(
            """
            Alice: 100
            ├──  Bob: 3
            ├──  Charlie: 5
            │  ├──  Charlie.A: 1
            │  ├──  Charlie.B: -
            │  └──  Charlie.C: 2
            │     ├──  Echo: 7
            │     └──  Foxtrot: -5
            └──  Daniel: 2
            """
        ),  # fmt: skip
    )
    return
