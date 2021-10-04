# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from datetime import datetime;
from datetime import timedelta;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Timer(object):
    _timeelapsed: timedelta;
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
        self._timeelapsed += (t1 -  t0);
        return self;

    def reset(self):
        t = datetime.now();
        self._timeelapsed = t - t;
        self._timecurrent = t;
        return self;

    @property
    def elapsed(self) -> timedelta:
        return self._timeelapsed;
