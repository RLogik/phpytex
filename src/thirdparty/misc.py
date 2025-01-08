#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

# for modifications, not export
import re
import time
from copy import copy
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from functools import wraps
from itertools import product as itertools_product
from textwrap import dedent as textwrap_dedent
from typing import Any
from typing import Callable
from typing import TypeVar

# import lorem
import pytz
from codetiming import Timer as TimerBasic
from codetiming import TimerError
from pydantic import AwareDatetime

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "AwareDatetime",
    "Timer",
    "TimerError",
    "TimerQuiet",
    "copy",
    "datetime",
    "dedent",
    "dedent_full",
    "dedent_split",
    "deepcopy",
    "get_date_stamp",
    "get_datetime_stamp",
    "get_timestamp",
    "itertools_product",
    # 'lorem',
    "make_aware_datetime",
    "make_aware_datetime_or_none",
    "parse_datetime",
    "pytz",
    "re",
    "reindent_lines",
    "strip_around",
    "timedelta",
    "timezone",
    "unindent_lines",
    "unindent_text",
]

# ----------------------------------------------------------------
# MODIFICATIONS
# ----------------------------------------------------------------


def parse_datetime(stamp: str) -> datetime:
    return datetime.fromisoformat(stamp.replace("Z", " +00:00"))


def get_timestamp(format: str = r"%Y-%m-%d %H:%M:%S%z") -> str:
    return datetime.now().strftime(format)


def get_datetime_stamp(rounded: bool = False) -> str:
    return get_timestamp(r"%Y-%m-%d %H:%M:%S%z" if rounded else r"%Y-%m-%d %H:%M:%S.%f%z")


def get_date_stamp() -> str:
    return get_timestamp(r"%Y-%m-%d")


def make_aware_datetime(t: datetime, tz: timezone) -> AwareDatetime:
    """
    Returns a copy of a datetime object.

    - If the object was 'timezone-aware' then the clone is returned.
    - Otherwise forcibly adds timezone to clone and returns this.
    """
    # DEV-NOTE: returns a clone, does not change original variable
    return t.replace(tzinfo=t.tzinfo or tz)


def make_aware_datetime_or_none(t: Any, tz: timezone) -> AwareDatetime | None:
    """
    Makes a datetime timezone-aware.
    """
    if not isinstance(t, datetime):
        return None
    return make_aware_datetime(t=t, tz=tz)


class Timer(TimerBasic):
    @property
    def elapsed(self) -> float:
        self.last = time.perf_counter() - self._start_time
        return self.last


class TimerQuiet:
    """
    A class to simply compute elapsed time without any logging
    """

    _current_time = 0

    def __init__(self):
        return

    def start(self):
        self._current_time = time.perf_counter()

    def stop(self) -> float:
        t = time.perf_counter()
        dt = t - self._current_time
        self._current_time = t
        return dt


def strip_around(
    text: str,
    first: bool,
    last: bool,
    all: bool = True,
):
    """
    Strips all initial/final 'empty' lines.
    """
    lines = re.split(pattern=r"\n", string=text)
    if all:
        if first:
            while len(lines) > 0 and lines[0].strip() == "":
                lines = lines[1:]
        if last:
            while len(lines) > 0 and lines[-1].strip() == "":
                lines = lines[:-1]
    else:
        if first:
            lines = lines[1:]
        if last:
            lines = lines[:-1]
    text = "\n".join(lines)
    return text


def dec_prestrip(first: bool = True, last: bool = True, all: bool = False):
    """
    Returns a decorator that modifies string -> string methods
    """
    T = TypeVar("T")

    def dec(method: Callable[[str], T]) -> Callable[[str], T]:
        """
        Performs method but first strips all initial/final 'empty' lines.
        """

        @wraps(method)
        def wrapped_method(text: str) -> T:
            text = strip_around(text, first=first, last=last, all=all)
            return method(text)

        return wrapped_method

    return dec


@dec_prestrip(all=False)
def dedent(text: str) -> str:
    r"""
    Remove any common leading whitespace from every line in `text`.

    This can be used to make triple-quoted strings line up with the left
    edge of the display, while still presenting them in the source code
    in indented form.

    Note that tabs and spaces are both treated as whitespace, but they
    are not equal: the lines "  hello" and "\\thello" are
    considered to have no common leading whitespace.

    Entirely blank lines are normalised to a newline character.

    NOTE: this method trims the 1st and last lines.

    ## Examples ##

    ```py
    text = dedent(
        '''
          This is a text
        ==============

        Here are the contents

          - item 1
          - item 2
          - item 3
        '''
    )
    print(f'\\n{text}\\n')
    ```
    results in
    ```text
    ----
        This is a text
    ==============

    Here are the contents

        - item 1
        - item 2
        - item 3
    ----
    ```
    whereas
    ```py
    text = dedent(
        '''


          This is a text
        ==============

        Here are the contents

          - item 1
          - item 2
          - item 3

        '''
    )
    print(f'\\n{text}\\n')
    ```
    results in
    ```text
    ----


        This is a text
    ==============

    Here are the contents

        - item 1
        - item 2
        - item 3

    ----
    ```
    """
    return textwrap_dedent(text)


@dec_prestrip(all=True)
def dedent_full(text: str) -> str:
    r"""
    Remove any common leading whitespace from every line in `text`.

    This can be used to make triple-quoted strings line up with the left
    edge of the display, while still presenting them in the source code
    in indented form.

    Note that tabs and spaces are both treated as whitespace, but they
    are not equal: the lines "  hello" and "\\thello" are
    considered to have no common leading whitespace.

    Entirely blank lines are normalised to a newline character.

    NOTE: this method completely strips all pre/post empty lines
    (= lines containing at most only white spaces).

    ## Examples ##

    ```py
    text = dedent_full(
        '''
          This is a text
        ==============

        Here are the contents

          - item 1
          - item 2
          - item 3
        '''
    )
    print(f'\\n{text}\\n')
    ```
    results in
    ```text
    ----
        This is a text
    ==============

    Here are the contents

        - item 1
        - item 2
        - item 3
    ----
    ```
    and
    ```py
    text = dedent_full(
        '''


          This is a text
        ==============

        Here are the contents

          - item 1
          - item 2
          - item 3

        '''
    )
    print(f'\\n{text}\\n')
    ```
    results in
    ```text
    ----
        This is a text
    ==============

    Here are the contents

        - item 1
        - item 2
        - item 3
    ----
    ```
    """
    return textwrap_dedent(text)


def dedent_split(text: str, full: bool = False) -> list[str]:
    text = dedent_full(text) if full else dedent(text)
    return re.split(r"\r?\n", text)


def unindent_text(text: str, reference: str = "") -> str:
    text = f"\n{reference}.\n{text}\n"  # add reference point to first line
    lines = dedent_split(text)  # dedent, utilising the reference marker
    lines = lines[1:]  # strip reference marker
    text = "\n".join(lines)
    return text


def unindent_lines(lines: list[str], reference: str = "") -> list[str]:
    text = "\n".join(lines)
    text = f"\n{reference}.\n{text}\n"  # add reference point to first line
    lines = dedent_split(text)  # dedent, utilising the reference marker
    return lines[1:]  # strip reference marker


def reindent_lines(lines: list[str], indent: str, unindent: bool = False) -> list[str]:
    """
    Either adds to indentation (`unindent=False`)
    or forces an indentation level (`unindent=True`).
    """
    if unindent:
        lines = unindent_lines(lines)
    return [indent + line for line in lines]
