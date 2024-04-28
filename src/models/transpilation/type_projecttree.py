#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

from ...thirdparty.system import *
from ...thirdparty.types import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    'ProjectTree',
]

# ----------------------------------------------------------------
# CLASS EvalType for usage with yaml
# ----------------------------------------------------------------


class ProjectTree(object):
    _files: list[str]
    _directories: dict[str, ProjectTree]

    def __init__(self, **kwargs):
        files = []
        for key in ['files', 'file']:
            if key in kwargs and (kwargs[key] is None or isinstance(kwargs[key], list)):
                files = kwargs[key] or []
                break
        assert all(
            isinstance(file, str) for file in files
        ), 'Component \033[1mfiles:\033[0m must be a list of strings.'
        directories = dict()
        for key in ['folders', 'directories', 'components']:
            if key in kwargs and (kwargs[key] is None or isinstance(kwargs[key], dict)):
                directories = kwargs[key] or {}
                directories = {path: (struct or {}) for path, struct in directories.items()}
                break

        self._files = files or []
        self._directories = {
            path: ProjectTree(**struct) for path, struct in directories.items()
        }
        return

    def directories(self, path: str = '') -> Generator[str, None, None]:
        for subpath, obj in self._directories.items():
            yield os.path.join(path, subpath)
        for subpath, obj in self._directories.items():
            yield from obj.directories(path=os.path.join(path, subpath))
        return

    def files(self, path: str = '') -> Generator[str, None, None]:
        for file in self._files:
            yield os.path.join(path, file)
        for subpath, obj in self._directories.items():
            yield from obj.files(path=os.path.join(path, subpath))
        return

    @property
    def representation(self) -> dict[str, Any]:
        return dict(
            files=self._files,
            folders={path: obj.representation for path, obj in self._directories.items()},
        )

    def __str__(self) -> str:
        return str(self.representation)
