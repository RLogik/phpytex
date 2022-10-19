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
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FUNCTION_NAME_MAIN = '____phpytex_main';
FUNCTION_NAME_FILE = '____phpytex_generate_file';
FUNCTION_NAME_PRE  = '____phpytex_generate_pre';
PATH_TO_VERSION       = 'assets/VERSION';
PATH_TO_TEMPLATE_PRE  = 'assets/template_pre';
PATH_TO_TEMPLATE_POST = 'assets/template_post';
PATH_TO_GRAMMAR       = 'assets/phpytex.lark';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LAZY LOADED RESOURCES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# extract from data assets + app configuration

def load_assets_config() -> Config: # pragma: no cover
    with open(PATH_ASSETS_CONFIG, 'r') as fp:
        assets = yaml_to_js_dictionary(yaml_load(fp, Loader=yaml_FullLoader), deep=True);
        assert isinstance(assets, dict);
        return Config(**assets);

def load_assets_languages(default: str) -> TranslatedTexts: # pragma: no cover
    with open(PATH_ASSETS_LANGUAGE, 'r') as fp:
        assets = yaml_load(fp, Loader=yaml_FullLoader);
        assert isinstance(assets, dict);
        return TranslatedTexts(assets=assets, on_missing=ON_MISSING, default=default);

# use lazy loaing to ensure that values only loaded (once) when used
CONFIG = lazy(load_assets_config);
OPTIONS = lazy(lambda x: x.app_options, CONFIG);
COMMANDS = lazy(lambda x: Commands(x.commands), CONFIG);
LANGUAGE_CODES = lazy(lambda x: LanguagePatterns(x.language_codes), CONFIG);
SUPPORTED_LANGUAGES = lazy(lambda x: x.keys, LANGUAGE_CODES);
DEFAULT_LANGUAGE = lazy(lambda x: x.default_language, OPTIONS);

TRANSLATIONS = lazy(load_assets_languages, default=DEFAULT_LANGUAGE);
