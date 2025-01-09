#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from datetime import datetime
from datetime import timedelta
from datetime import timezone

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "Countdown",
]

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class Countdown:
    """
    Allows one to set events based on a timer.
    """

    _duration: float
    _time_finished: datetime

    def __init__(self, duration: float):
        self._duration = duration
        self.restart()

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def time_finished(self) -> datetime:
        return self._time_finished

    @property
    def done(self) -> bool:
        """
        Checks if countdown timer is finished.

        - if done, returns `true`.
        - otherwise returns `false`.
        """
        t_now = datetime.now(timezone.utc)
        return t_now >= self._time_finished

    def restart_if_done(self) -> bool:
        """
        Checks if countdown timer is finished.

        - if done, resets and returns `true`.
        - otherwise returns `false`.
        """
        if self.done:
            self.restart()
            return True
        return False

    def restart(self):
        """
        Restarts the timer.
        """
        dt = self.duration  # in seconds
        t_now = datetime.now(timezone.utc)
        self._time_finished = t_now + timedelta(seconds=dt)
        return
