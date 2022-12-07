#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.models.generated.user import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ProjectTree',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Project Tree
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProjectTree(DataTypeFolder):
    @property
    def representation(self) -> dict[str, Any]:
        return dict(
            files=self.files,
            folders={ path: obj.representation for path, obj in self.directories.items() },
        );

    def __str__(self) -> str:
        return str(self.representation);

    def get_directories(self, path: str = '') -> Generator[str, None, None]:
        for subpath, obj in self.folders.items():
            yield os.path.join(path, subpath);
        for subpath, obj in self.folders.items():
            yield from obj.folders(path=os.path.join(path, subpath));
        return;

    def get_files(self, path: str = '') -> Generator[str, None, None]:
        for file in self.files:
            yield os.path.join(path, file);
        for subpath, obj in self.directories.items():
            yield from obj.get_files(path=os.path.join(path, subpath));
        return;
