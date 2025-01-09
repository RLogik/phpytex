#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import time

from codetiming import Timer as TimerBasic

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "Timer",
    "TimerQuiet",
]

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


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
