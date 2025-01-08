#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import json
import os
from base64 import b64decode
from base64 import b64encode
from hashlib import sha256
from io import BytesIO
from zipfile import ZipFile

import yaml

from ...models.datasources import *
from .io_yaml import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "BytesIOStream",
    "decode_base_64",
    "encode_base_64",
    "hash_encode",
    "parse_contents",
    "read_internal_asset",
    "read_yaml",
    "read_yaml_from_contents",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def hash_encode(text: str, encoding: ENCODING = "utf-8") -> bytes:
    """
    Note:
    A hash encoded value cannot (under current computational methods)
    be effectively decoded.
    They can 'only' be used to check if an entered value
    matches another previously safely stored value (e.g. a password),
    by comparing their hashes.

    """
    return sha256(text.encode(encoding)).hexdigest().encode("ascii")


def encode_base_64(text: str, encoding: ENCODING = "utf-8") -> str:
    return b64encode(text.encode(encoding)).decode("ascii")


def decode_base_64(code: str, encoding: ENCODING = "utf-8") -> str:
    try:
        return b64decode(code.encode("ascii")).decode(encoding)

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


def read_yaml(path: str):
    """
    Reads yaml from a path and uses custom registered constructors for parsing.
    """
    register_yaml_constructors()
    with open(path, "rb") as fp:
        assets = yaml.load(fp, Loader=yaml.FullLoader)
        return assets


def read_yaml_from_contents(contents: bytes):
    """
    Reads yaml from bytes and uses custom registered constructors for parsing.
    """
    register_yaml_constructors()
    with BytesIOStream(contents) as fp:
        assets = yaml.load(fp, Loader=yaml.FullLoader)
        return assets


def parse_contents(
    contents: bytes,
    /,
    *,
    format: BASIC_FILETYPES,
):
    match format:
        case ".yaml":
            # read from contents (assumed to be in yaml-format)
            return read_yaml_from_contents(contents)

        case ".json":
            # read from contents (assumed to be in yaml-format)
            return json.loads(contents)

        case _:
            raise ValueError(f"No read method developed for {format}")


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
