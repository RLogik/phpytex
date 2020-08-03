#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from yaml import load;
from yaml import FullLoader;
from typing import Any;
from typing import Dict;
from typing import List;
from typing import Tuple;
from typing import Union;

from ..__path__ import project_path;
from ..core.utils import static;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class Struct
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Struct:
    @static
    def NAME_KEY(cls):
        return 'name';

    __struct: Union[None, Dict[str, Any]];

    def __init__(self, fname: str = None, struct: Dict[str, Any] = None, **kwargs):
        if not fname is None:
            self.fromFile(fname);
        elif not struct is None:
            self.__struct = struct;
        else:
            self.__struct = dict();
        return;

    @classmethod
    def get_from_file(cls, fname: str) -> Dict[str, Any]:
        try:
            with open(project_path(fname), 'r') as fp:
                struct = load(fp, Loader=FullLoader);
        except:
            struct = dict();
        return struct;

    @classmethod
    def get_value(cls, obj: Any, key: str, *keys: str, default: Any = None) -> Any:
        obj_ = obj[key] if isinstance(obj, dict) and key in obj else default;
        return obj_ if len(keys) == 0 else cls.get_value(obj_, *keys);

    @classmethod
    # extracts name of attribute --- either the key itself, or the 'name' attribute, if defined.
    def get_name(cls, struct: Any, key: str) -> str:
        return cls.get_value(struct, Struct.NAME_KEY, default=key);

    @classmethod
    def get_parts(cls, struct: Union[Dict[str, Any], List[str]]) -> List[Tuple[str, str, Any]]:
        if isinstance(struct, list):
            return [(key, key, {}) for key in struct];
        return [(key, cls.get_name(struct[key], key), struct[key]) for key in struct];

    def fromFile(self, fname: str):
        self.__struct = Struct.get_from_file(fname);
        return;

    def getValue(self, *keys: str, default=None):
        return Struct.get_value(self.__struct, *keys, default=default);

    def getName(self, *keys: str) -> str:
        n = len(keys);
        key = keys[n-1] if n > 0 else None;
        return self.getValue(*keys, Struct.NAME_KEY, default=key);

    def getParts(self, *keys: str) -> List[Tuple[str, str, Any]]:
        if len(keys) == 0:
            struct = self.__struct;
        else:
            struct = self.getValue(*keys, default={});
        if isinstance(struct, list):
            return [(str(key), str(key), {}) for key in struct];
        elif isinstance(struct, dict):
            return [(key, Struct.get_name(struct[key], key), struct[key]) for key in struct];
        return [];
