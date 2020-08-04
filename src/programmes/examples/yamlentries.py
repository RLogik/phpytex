#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any;
from typing import Dict;
from typing import List;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Auxiliary Class: YamlEntry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class YamlEntry:
    depth: int;
    key: str;
    multiline: bool;
    value: Any;
    comment: str;

    def __init__(self, key: str, depth=0, multiline=False, value=None, comment=None, **kwargs):
        self.key = key;
        self.depth = depth
        self.multiline = multiline;
        if multiline:
            self.value = [];
            if isinstance(value, list):
                self.value = value;
        else:
            self.value = value;
        if isinstance(comment, str):
            self.comment = comment;

    def __str__(self):
        indent = '  '*self.depth;
        key_string = '\033[94m{}\033[0m'.format(self.key);
        comment_string = ' \033[32m# {}\033[0m'.format(self.comment) if hasattr(self, 'comment') else '';
        if self.multiline:
            lines = [];
            lines.append(indent + '{}: \033[1m|-\033[0m{}'.format(key_string, comment_string));
            for val in self.value:
                lines.append(indent + '  \033[1m{}\033[0m'.format(val));
            return '\n'.join(lines);
        else:
            value_string = ' \033[1m{}\033[0m'.format(self.value) if not(self.value is None) else '';
            return indent + '{}:{}{}'.format(key_string, value_string, comment_string);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Auxiliary Class: YamlEntries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class YamlEntries:
    depth: int;
    __entries: Dict[str, List[YamlEntry]];

    def __init__(self):
        self.depth = 0;
        self.__entries = dict();
        pass;

    def __iter__(self):
        for key in self.__entries:
            entries = self.__entries[key];
            for k, entry in enumerate(entries):
                yield key, k, entry;

    def __str__(self):
        return '\n'.join([str(entry) for _, _, entry in self.__iter__()]);

    def push(self):
        self.depth += 1;
        return;

    def pop(self):
        self.depth = max(self.depth - 1, 0);
        return;

    def add(self, key: str, entry=None, multiline=False, value=None, comment=None, **kwargs):
        if not key in self.__entries:
            self.__entries[key] = [];
        if isinstance(entry, YamlEntry):
            self.__entries[key].append(entry);
        else:
            self.__entries[key].append(YamlEntry(key=key, depth=self.depth, multiline=multiline, value=value, comment=comment));
        return;
