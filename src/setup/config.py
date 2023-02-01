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
    'CONFIG',
    'ASSETS',
    'NAMESPACE',
    'PATHS',
    'TRANSPILATION',
    'load_user_config',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LAZY LOADED RESOURCES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@make_lazy
def load_internal_config() -> ProgrammeConfig: # pragma: no cover
    with open(src.paths.config, 'r') as fp:
        assets = yaml_load(fp, Loader=YamlFullLoader);
        assert isinstance(assets, dict);
        return ProgrammeConfig(**assets);

def load_user_config(file_config: Optional[str]) -> UserConfig:
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
        object = yaml_load(fp, Loader=YamlFullLoader);
        assert isinstance(object, dict);
        return UserConfig(**object);

# use lazy loaing to ensure that values only loaded (once) when used
CONFIG: ProgrammeConfig = load_internal_config();
ASSETS: AssetsPaths = lazy(lambda: CONFIG.assets);
NAMESPACE: NameSpacePython = lazy(lambda: CONFIG.namespace);
PATHS: PathSettings = lazy(lambda: CONFIG.paths);
TRANSPILATION: TranspileOptions = lazy(lambda: CONFIG.transpile);
