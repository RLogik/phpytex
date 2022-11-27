# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Timer(object):
    _time_elapsed: timedelta;
    _timecurrent: datetime;

    def __init__(self):
        self.reset();

    def __str__(self) -> str:
        return str(self.elapsed);

    def start(self):
        self._timecurrent = datetime.now();
        return self;

    def stop(self):
        t0 = self._timecurrent;
        t1 = datetime.now();
        self._timecurrent = t1;
        self._time_elapsed += (t1 -  t0);
        return self;

    def reset(self):
        t = datetime.now();
        self._time_elapsed = t - t;
        self._timecurrent = t;
        return self;

    @property
    def elapsed(self) -> timedelta:
        return self._time_elapsed;
