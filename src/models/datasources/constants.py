#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from enum import StrEnum
from typing import Literal

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "BASIC_FILETYPES",
    "ENCODING",
    "MIME_TYPE",
]

# ----------------------------------------------------------------
# CLASSES / CONSTANTS
# ----------------------------------------------------------------

ENCODING = Literal[
    "ascii",
    "utf-8",
    "unicode_escape",
]


class MIME_TYPE(StrEnum):
    BYTES = "application/octet-stream"
    TEXT = "text/plain;charset=utf-8"
    JSON = "application/json;charset=utf-8"
    # see https://learn.microsoft.com/previous-versions/office/office-2007-resource-kit/ee309278(v=office.12)
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


BASIC_FILETYPES = Literal[
    ".json",
    ".yaml",
    ".csv",
    ".xlsx",
    ".pdf",
    ".txt",
]
