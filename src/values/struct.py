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

    __struct: Dict[str, Any];

    def __init__(self, fname: str = None, struct: Dict[str, Any] = None, internal: bool = False, **kwargs):
        if not fname is None:
            self.__struct = Struct.get_from_file(fname, internal=internal);
        elif isinstance(struct, dict):
            self.__struct = struct;
        else:
            self.__struct = dict();
        return;

    def __str__(self):
        return str(self.__struct);

    def __iter__(self):
        for key in self.__struct:
            yield key, self.__struct[key];

    @classmethod
    def get_from_file(cls, fname: str, internal: bool = False) -> Dict[str, Any]:
        try:
            with open(project_path(fname) if internal else fname, 'r') as fp:
                spec = load(fp, Loader=FullLoader);
        except:
            spec = dict();
        return spec;

    @classmethod
    def get_value(cls, obj: Any, key: str, *keys: str, default: Any = None) -> Any:
        # overwrites [missing key as well as None (=key defined but value)] by 'default':
        if isinstance(obj, dict) and key in obj:
            obj_ = obj[key];
            if len(keys) == 0:
                return default if obj_ is None else obj_;
            return cls.get_value(obj_, *keys, default=default);
        else:
            return default;

    @classmethod
    # extracts name of attribute --- either the key itself, or the 'name' attribute, if defined.
    def get_name(cls, struct: Any, key: str) -> str:
        return cls.get_value(struct, Struct.NAME_KEY, default=key);

    @classmethod
    def get_parts(cls, struct: Union[Dict[str, Any], List[str]]) -> List[Tuple[str, str, Any]]:
        if isinstance(struct, list):
            return [(key, key, {}) for key in struct];
        return [(key, cls.get_name(struct[key], key), struct[key]) for key in struct];

    def getSubStruct(self, *keys: str):
        spec = self.getValue(*keys, default=dict());
        return Struct(struct=spec);

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
