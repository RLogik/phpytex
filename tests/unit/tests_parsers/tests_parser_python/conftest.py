#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from tests.unit.thirdparty.fake import *
from tests.unit.thirdparty.unit import *

from src._core.utils.misc import *

# ----------------------------------------------------------------
# FIXTURES
# ----------------------------------------------------------------


@fixture(scope="function", autouse=False)
def codelines0a() -> str:
    return dedent(
        """
        for x, y in [
            ("ant", 4),
            ("cat", 1),
            (None, 5),
            ("elephant", 2),
        ]:
        """
    )


@fixture(scope="function", autouse=False)
def codelines0b() -> str:
    return dedent(
        """
        for x, y in [
            ("ant", 4),
            ("cat", 1),
            (None, 5),
            ("elephant", 2),
        ]:
            if x is not None:
        """
    )


@fixture(scope="function", autouse=False)
def codelines0c() -> str:
    return dedent(
        """
        for x, y in [
            ("ant", 4),
            ("cat", 1),
            (None, 5),
            ("elephant", 2),
        ]:
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                if True:
                                    pass
            if x is not None:
                if y > 1:
        """
    )


@fixture(scope="function", autouse=False)
def codelines1a() -> str:
    return dedent(
        """
            # from a previous line
            y = 0

        for x, y in [
            ("ant", 4),
            ("cat", 1),
            (None, 5),
            ("elephant", 2),
        ]:
            if x is not None:
        """
    )


@fixture(scope="function", autouse=False)
def codelines1b() -> str:
    return dedent(
        """
                # from a previous line
                y = 0

        for x, y in [
            ("ant", 4),
            ("cat", 1),
            # comment1
            (None, 5),
            ("elephant", 2),
        ]: # comment3
            if x is not None:
                if y > 1:
        """
    )


@fixture(scope="function", autouse=False)
def codelines2a() -> str:
    return dedent(
        """
                # from a previous line
                y = 0

        if False:
            if True:
                if True:
                    # some comment
                    x = 0

        for x, y in [
            ("ant", 4),
            ("cat", 1),
            # comment1
            (None, 5),
            ("elephant", 2),
        ]: # comment3
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                if True:
                                    pass
            if x is not None:
                if True:
                    if y > 1: # some comment
        """
    )


@fixture(scope="function", autouse=False)
def codelines2b() -> str:
    return dedent(
        """
                # from a previous line
                y = 0

        if False:
            if True:
                if True:
                    # some comment
                    x = 0

        for x, y in [
            ("ant", 4),
            ("cat", 1),
            # comment1
            (None, 5),
            ("elephant", 2),
        ]: # comment3
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                if True:
                                    pass
            if x is not None:
                if True:
                    if y > 1: # some comment
                        # some other comment
        """
    )
