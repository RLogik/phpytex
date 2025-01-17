#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
import platform
import re
import subprocess
from pathlib import Path

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "clear_dir_if_exists",
    "create_dir_if_not_exists",
    "create_file_if_not_exists",
    "is_linux",
    "pipe_call",
    "python_command",
    "remove_dir_if_exists",
    "remove_file_if_exists",
    "write_text_file",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def create_dir_if_not_exists(path: str | Path, /) -> bool:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p.exists()


def create_file_if_not_exists(path: str | Path, /) -> bool:
    p = Path(path)
    create_dir_if_not_exists(p.parent)
    # ----------------
    # NOTE: set
    # 1. read+write access (=6) for user
    # 2. read+write access (=6) for group
    # 3. read access (=4) for others
    # ----------------
    p.touch(mode=0o664, exist_ok=True)
    return p.exists()


def clear_dir_if_exists(path: str | Path) -> bool:
    p = Path(path) if isinstance(path, str) else path
    if not (p.exists() and p.is_dir()):
        return True

    # DEV-NOTE: yields actual paths, not just names relative to current path.
    subpaths = [q for q in p.iterdir() if q.is_dir()]
    files = [q for q in p.iterdir() if q.is_file()]

    success = True

    # delete folders first
    for subpath in subpaths:
        success = remove_dir_if_exists(subpath) and success

    # then delete files
    for subpath in files:
        success = remove_file_if_exists(subpath) and success

    return success


def remove_dir_if_exists(path: str | Path) -> bool:
    p = Path(path) if isinstance(path, str) else path
    if not p.exists():
        return True
    clear_dir_if_exists(p)
    p.rmdir()
    return not p.exists()


def remove_file_if_exists(path: str | Path) -> bool:
    p = Path(path) if isinstance(path, str) else path
    p.unlink(missing_ok=True)
    return not p.exists()


def write_text_file(
    path: str,
    lines: list[str],
    trim_empty_lines: bool = True,
    add_empty_line: bool = True,
):
    """
    Writes lines of text to file.
    """
    create_file_if_not_exists(path)

    # trim lines
    if trim_empty_lines:
        lines = lines[:]
        while len(lines) > 0 and re.match(r"^\s*$", lines[-1]):
            lines = lines[:-1]

    # write lines
    with open(path, "w") as fp:
        fp.write("\n".join(lines))
        if add_empty_line:
            fp.write("\n")
    return


def is_linux() -> bool:
    # return not ( os.name == 'nt' );
    return not (platform.system().lower() == "windows")


def python_command() -> str:
    return "python3" if is_linux() else "py -3"


def pipe_call(
    args: list[str],
    cwd=None,
    err_msg: str = "",
    fname_out: str | None = None,
):
    """
    DEV-NOTE: subprocess.run is like subprocess.Popen but waits for result
    """
    cwd = cwd if isinstance(cwd, str) else os.getcwd()
    if fname_out is None:
        result = subprocess.run(args, cwd=cwd)
    else:
        with open(fname_out, "w") as fp:
            result = subprocess.run(args, cwd=cwd, stdout=fp)
    if result.returncode == 0:
        return

    err_msg = err_msg or f"Shell command < \033[94;1m{' '.join(args)}\033[0m > failed."
    raise Exception(err_msg)
