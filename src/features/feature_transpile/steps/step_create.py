#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
import re
from typing import Any

from ...._core.logging import *
from ...._core.utils.basic import *
from ...._core.utils.system import *
from ....models.transpilation import *
from ....models.user import *
from ....parsers import parser_python
from ....queries import user
from ....setup import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "step_create",
]

# ----------------------------------------------------------------
# METHOD: step create
# ----------------------------------------------------------------


@echo_function(tag="STEP CREATE AUXILIARY FILES", level="INFO", close=True)
def step_create(cfg_user: UserConfig):
    """
    Step to create auxiliary files.
    """
    create_project_tree(path=os.getcwd(), files=cfg_user.files, folders=cfg_user.folders)

    if cfg_user.stamp is not None:
        create_file_stamp(
            path=cfg_user.stamp.file,
            overwrite=cfg_user.stamp.overwrite,
            options=cfg_user.stamp.options,
        )

    if cfg_user.parameters is not None:
        create_parameter_encoding(options=cfg_user.parameters.options)

    return


# ----------------------------------------------------------------
# SECONDARY METHODS
# ----------------------------------------------------------------


def create_project_tree(path: str, files: list[str], folders: dict[str, UserProjectTree]):
    """
    Breadth-first recursive creation of user project tree.
    """
    for relfname in files:
        if not create_file_if_not_exists(os.path.join(path, relfname)):
            raise FileExistsError(f"Could not create file \033[1m{relfname}\033[0m")

    for relpath, _ in folders.items():
        subpath = os.path.join(path, relpath)
        if not create_dir_if_not_exists(os.path.join(path, relpath)):
            raise FileExistsError(f"Could not create (sub)folder \033[1m{relpath}\033[0m")

    for relpath, tree in folders.items():
        subpath = os.path.join(path, relpath)
        create_project_tree(path=subpath, files=tree.files, folders=tree.folders)
    return


def create_file_stamp(
    path: str,
    overwrite: bool,
    options: dict[str, Any],
):
    if os.path.exists(path) and not overwrite:
        return

    lines = []
    border = r"%% " + "*" * 80
    max_tag_length = max([0] + [len(key) for key in options])

    for key in options:
        value = options[key]
        tag = key.upper()
        line = r"%% " + tag + r":"
        if isinstance(value, str):
            value = re.split("\n", str(value))

        elif isinstance(value, (int, float, bool)):
            value = [str(value)]

        if isinstance(value, list) and len(value) == 1:
            line += " " * (1 + max_tag_length - len(tag)) + str(value[0])

        elif isinstance(value, list) and len(value) > 1:
            indent = "\n" + r"%% " + " " * 4
            line_ = [""]
            line_ += [u for u in value if isinstance(u, str)]
            line += indent.join(line_)

        else:
            line += " " * (1 + max_tag_length - len(tag)) + r"—"

        lines.append(line)

    if len(lines) > 0:
        lines = [border, *lines, border]

    write_text_file(path=path, lines=lines)
    return


def create_parameter_encoding(options: dict[str, Any]):
    # unparse key-values
    data = [
        (name, value, parser_python.unparse(value, indent=0, multiline=False))
        for name, value in options.items()
    ]
    # clean keys
    user.EXPORT_VARS = {
        clean_var_name(name): (value, coded_value)
        for name, value, coded_value in data
    }  # fmt: skip
    return


# ----------------------------------------------------------------
# AUXILIARY METHODS
# ----------------------------------------------------------------


def clean_var_name(key: str) -> str:
    return re.sub(r"[^a-z0-9\_]", "_", key, flags=re.IGNORECASE)
