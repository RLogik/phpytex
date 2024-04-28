#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from enum import Enum

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'MimeType',
]

# ----------------------------------------------------------------
# ENUMS
# ----------------------------------------------------------------


class MimeType(Enum):
    BYTES = 'application/octet-stream'
    TEXT = 'text/plain;charset=utf-8'
    JSON = 'application/json;charset=utf-8'
    # see https://learn.microsoft.com/previous-versions/office/office-2007-resource-kit/ee309278(v=office.12)
    XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
