#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import src.paths;

from src.thirdparty.misc import *;
from src.thirdparty.config import *;
from src.thirdparty.code import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.models.config import *;
from src.models.user import *;
from src.core.utils import *;
from src.setup.yaml import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'APP_CONFIG',
    'ASSET_PATHS',
    'COMPILE_OPTIONS',
    'PATHS',
    'load_user_config',
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

ASSET_PATHS = AssetPaths(
    version = 'dist/VERSION',
    template_pre = 'assets/template_pre',
    template_post = 'assets/template_post',
    grammar = 'assets/phpytex.lark',
);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LAZY LOADED RESOURCES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_internal_config() -> ProgrammeConfig: # pragma: no cover
    with open(src.paths.config, 'r') as fp:
        assets = yaml_load(fp, Loader=yaml_FullLoader);
        assert isinstance(assets, dict);
        return ProgrammeConfig(**assets);

def load_user_config(file_config: Optional[str]) -> UserConfig:
    setup_yaml_reader();
    pattern = PATHS.pattern_config;

    try:
        if file_config is None or file_config == '':
            file_config = get_files_by_pattern(
                path = src.paths.wd,
                pattern = pattern,
            )[0];
    except:
        raise Exception('Could not find or read any phpytex configuration files.');

    assert os.path.exists(file_config) and os.path.isfile(file_config), 'Config file must exist!';
    with open(file_config, 'r') as fp:
        object = yaml_load(fp, Loader=yaml_FullLoader);
        assert isinstance(object, dict);
        return UserConfig(**object);

# use lazy loaing to ensure that values only loaded (once) when used
APP_CONFIG: ProgrammeConfig = lazy(load_internal_config);
PATHS: ProgrammePaths = lazy(lambda: APP_CONFIG.paths);
COMPILE_OPTIONS: CompileOptions = lazy(lambda: APP_CONFIG.compilation);
# GRAMMAR = lazy
