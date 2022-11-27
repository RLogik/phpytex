#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.misc import *;
from src.thirdparty.config import *;
from src.thirdparty.code import *;
from src.thirdparty.types import *;

from src.models.config import *;
from src.core.utils import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'APP_CONFIG',
    'FILE_OPTIONS',
    'COMPILE_OPTIONS',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FUNCTION_NAME_MAIN = '____phpytex_main';
FUNCTION_NAME_FILE = '____phpytex_generate_file';
FUNCTION_NAME_PRE  = '____phpytex_generate_pre';

@dataclass
class AssetPaths():
    version: str = field();
    template_pre: str = field();
    template_post: str = field();
    grammar: str = field();
    config: str = field();

PATHS = AssetPaths(
    version = 'assets/VERSION',
    template_pre = 'assets/template_pre',
    template_post = 'assets/template_post',
    grammar = 'assets/phpytex.lark',
    config = 'assets/config.yaml'
);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LAZY LOADED RESOURCES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# extract from data assets + app configuration

def load_assets_config() -> ConfigParameters: # pragma: no cover
    with open(PATHS.config, 'r') as fp:
        assets = yaml_load(fp, Loader=yaml_FullLoader);
        assert isinstance(assets, dict);
        return ConfigParameters(**assets);

# use lazy loaing to ensure that values only loaded (once) when used
APP_CONFIG: ConfigParameters = lazy(load_assets_config);
FILE_OPTIONS: FileOptions = lazy(lambda x: x.files, APP_CONFIG);
COMPILE_OPTIONS: CompileOptions = lazy(lambda x: x.compilation, APP_CONFIG);
# GRAMMAR = lazy
