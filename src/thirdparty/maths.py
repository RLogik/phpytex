#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import math
import random
from fractions import Fraction

from numpy.random import MT19937
from numpy.random import RandomState
from numpy.random import SeedSequence

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------


def reseed(
    seed: int | None,
    legacy: bool = False,
) -> RandomState:
    rng = RandomState(MT19937(SeedSequence(seed)))
    if legacy:
        random.seed(seed)
    return rng


# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "Fraction",
    "math",
    "random",
    "reseed",
]
