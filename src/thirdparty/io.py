#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

# for modifications, not export
import os
import zlib
from argparse import ArgumentError
from argparse import ArgumentParser
from argparse import Namespace
from argparse import RawTextHelpFormatter
from base64 import b64decode
from base64 import b64encode
from enum import Enum
from getpass import getpass
from getpass import getuser
from hashlib import sha256
from io import BytesIO
from io import StringIO
from io import TextIOWrapper
from zipfile import ZipFile

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "ENCODING",
    "ArgumentError",
    "ArgumentParser",
    "BytesIO",
    "BytesIOStream",
    "Namespace",
    "RawTextHelpFormatter",
    "StringIO",
    "TextIOWrapper",
    "ZipFile",
    "b64decode",
    "b64encode",
    "decode_base_64",
    "encode_base_64",
    "getpass",
    "getuser",
    "hash_encode",
    "read_internal_asset",
    "sha256",
    "zlib",
]

# ----------------------------------------------------------------
# MODIFICATIONS
# ----------------------------------------------------------------


class ENCODING(Enum):
    ASCII = "ascii"
    UTF8 = "utf-8"
    UNICODE = "unicode_escape"


def hash_encode(text: str, encoding: ENCODING = ENCODING.UTF8) -> bytes:
    """
    Note:
    A hash encoded value cannot (under current computational methods)
    be effectively decoded.
    They can 'only' be used to check if an entered value
    matches another previously safely stored value (e.g. a password),
    by comparing their hashes.

    """
    return sha256(text.encode(encoding.value)).hexdigest().encode(ENCODING.ASCII.value)


def encode_base_64(text: str, encoding: ENCODING = ENCODING.UTF8) -> str:
    return b64encode(text.encode(encoding.value)).decode(ENCODING.ASCII.value)


def decode_base_64(code: str, encoding: ENCODING = ENCODING.UTF8) -> str:
    try:
        return b64decode(code.encode(ENCODING.ASCII.value)).decode(encoding.value)

    except Exception as _:
        return ""


class BytesIOStream:
    """
    Provides context manager for a bytes stream.
    """

    _contents: bytes

    def __init__(self, contents: bytes):
        self._contents = contents

    def __enter__(self):
        """
        Context manager for BytesIO that deals with seeking.
        """
        fp = BytesIO(self._contents).__enter__()
        fp.seek(0)
        return fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        return


def read_internal_asset(
    root: str,
    path: str,
    encoding: str = "utf-8",
    is_archived: bool = False,
) -> str:
    """
    Reads a file inside a folder that is optionally zipped.
    """
    if is_archived:
        with ZipFile(root, "r") as fp:
            return fp.read(path).decode(encoding)
    path = os.path.join(root, path)
    with open(path, "r") as fp:
        return "".join(fp.readlines())
