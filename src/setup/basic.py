#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging

from ..__paths__ import *
from .._core.logging import *
from .._core.utils.basic import *
from .._core.utils.code import *
from ..models.internal import *
from ..models.transpilation import *
from ..thirdparty.code import *
from ..thirdparty.config import *
from ..thirdparty.io import *
from ..thirdparty.maths import *
from ..thirdparty.misc import *
from ..thirdparty.system import *
from ..thirdparty.types import *

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
yaml_initialised = Property[bool]()
yaml_initialised.set(False)

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
    initialise_yaml_parser()
    logging.info(f"running {title or name} v{INFO.version} on PID {pid()}")
    return


def initialise_logging(name: str, debug: bool):
    level = "DEBUG" if debug else "INFO"
    path = path_logging()
    configure_logging(name=name, level=level, path=path)
    return


def initialise_yaml_parser():
    @make_safe_none
    def include_constructor(loader: yaml.Loader, node: yaml.Node):
        value = loader.construct_yaml_str(node)
        assert isinstance(value, str)
        args = value.split(r"/#/")
        path, keys_as_str = [*args, ""][:2]
        with open(path, "r") as fp:
            obj = yaml.load(fp, Loader=yaml.FullLoader)
        keys = keys_as_str.split("/")
        for key in keys:
            if key != "":
                obj = obj[key]

        return obj

    @make_safe_none
    def not_constructor(loader: yaml.Loader, node: yaml.Node) -> bool:
        value = loader.construct_yaml_bool(node)
        return not value

    @make_safe_none
    def key_constructor(loader: yaml.Loader, node: yaml.Node):
        value = loader.construct_sequence(node, deep=True)
        result = value[0]
        keys = value[1:]
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key, None)

            elif isinstance(key, int) and isinstance(result, (list, tuple)):
                result = result[key] if key < len(result) else None

            else:
                raise ValueError(f"Could not extract { '-> '.join(keys)} from {value[0]}")

        return result

    @make_safe(default="")
    def join_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
        values = loader.construct_sequence(node, deep=True)
        sep, parts = str(values[0]), [str(_) for _ in values[1]]
        return sep.join(parts)

    @make_safe(default_factory=lambda: EvalType())
    def eval_constructor(loader: yaml.Loader, node: yaml.Node) -> EvalType:
        value = loader.construct_sequence(node, deep=True)
        expr = value[0]
        assert isinstance(expr, str)
        return EvalType(expr)

    @make_safe_none
    def tuple_constructor(loader: yaml.Loader, node: yaml.Node) -> tuple:
        value = loader.construct_sequence(node, deep=True)
        return tuple(value)

    @make_safe_none
    def fraction_constructor(loader: yaml.Loader, node: yaml.Node) -> Fraction:
        value = loader.construct_yaml_str(node)
        return Fraction(value)

    yaml_initialised.set(True)
    yaml.add_constructor(tag="!include", constructor=include_constructor)
    yaml.add_constructor(tag="!eval", constructor=eval_constructor)
    yaml.add_constructor(tag="!not", constructor=not_constructor)
    yaml.add_constructor(tag="!join", constructor=join_constructor)
    yaml.add_constructor(tag="!key", constructor=key_constructor)
    yaml.add_constructor(tag="!tuple", constructor=tuple_constructor)
    yaml.add_constructor(tag="!fraction", constructor=fraction_constructor)
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
    text = read_internal_asset(
        root=get_root_path(),
        path=os.path.join("src", "setup", "config.yaml"),
        is_archived=open_source(),
    )
    assets = yaml.load(text, Loader=yaml.FullLoader)
    return AppConfig.model_validate(assets)


# ----------------------------------------------------------------
# LAZY LOADED RESOURCES
# ----------------------------------------------------------------
# NOTE: use lazy loading to ensure that values only loaded (once) when used

INFO = load_repo_info()
VERSION = get_version()
TIMEZONE = datetime.now().astimezone().tzinfo
APPCONFIG = load_internal_config()
