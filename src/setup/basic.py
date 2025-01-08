#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
import os
from datetime import datetime

import toml

from ..__paths__ import *
from .._core.logging import *
from .._core.utils.code import *
from .._core.utils.io import *
from ..models.internal import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "INFO",
    "VERSION",
]

# ----------------------------------------------------------------
# GLOBAL PROPERTIES
# ----------------------------------------------------------------

pid = FinalProperty[int]()
path_env = FinalProperty[str]()
path_logging = FinalProperty[str | None]()
quiet_mode = FinalProperty[bool]()
open_source = FinalProperty[bool]()

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def initialise_application(
    name: str,
    title: str | None = None,
    debug: bool = False,
):
    """
    Initialises logging and displays information about programme + pid.
    """
    initialise_logging(name=name, debug=debug)
    logging.info(f"running {title or name} v{INFO.version} on PID {pid()}")
    return


def initialise_logging(name: str, debug: bool):
    level = "DEBUG" if debug else "INFO"
    path = path_logging()
    configure_logging(name=name, level=level, path=path)
    return


# ----------------------------------------------------------------
# QUERIES
# ----------------------------------------------------------------


@make_lazy
@compute_once
def load_repo_info() -> RepoInfo:
    text = read_internal_asset(
        root=get_root_path(),
        path="pyproject.toml",
        is_archived=open_source(),
    )
    config_repo = toml.loads(text)
    assets = config_repo.get("project", {})
    info = RepoInfo.model_validate(assets)
    return info


@make_lazy
@compute_once
def get_version() -> str:
    info = load_repo_info()
    return info.version


@make_lazy
@compute_once
def load_internal_config() -> AppConfig:
    contents = read_internal_asset(
        root=get_root_path(),
        path=os.path.join("src", "setup", "config.yaml"),
        is_archived=open_source(),
    ).encode()
    assets = read_yaml_from_contents(contents)
    return AppConfig.model_validate(assets)


# ----------------------------------------------------------------
# LAZY LOADED RESOURCES
# ----------------------------------------------------------------
# NOTE: use lazy loading to ensure that values only loaded (once) when used

INFO = load_repo_info()
VERSION = get_version()
TIMEZONE = datetime.now().astimezone().tzinfo
APPCONFIG = load_internal_config()
