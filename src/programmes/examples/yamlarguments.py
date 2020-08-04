#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re;
from typing import Any;
from typing import List;

from .yamlentries import YamlEntry;
from .yamlentries import YamlEntries;
from ...core.utils import to_python_key;
from ...info.arguments import display_value_type;
from ...types.parse import FlattenableType;
from ...types.parse import string_to_type;
from ...values.struct import Struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: YamlArgument
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class YamlArgument:
    entry: YamlEntry;
    label: str;
    labels: List[str];
    parent: str;
    depth: int;

    value_type: FlattenableType;
    description: str;
    is_part: bool;
    example_value: Any;

    def __init__(
        self,
        label: str,
        labels=None,
        parent=None,
        depth=None,
        value_type=None,
        description=None,
        is_part=False,
        example_value=None,
        **kwargs
    ):
        self.label = label;
        self.labels = [label];
        if isinstance(labels, List[str]):
            self.labels = labels;
        if isinstance(parent, str):
            self.parent = parent;
        if isinstance(depth, int):
            self.depth = depth;
        if isinstance(description, str):
            self.description = description;
        self.value_type = string_to_type(value_type);
        self.example_value = example_value;
        self.is_part = is_part;
        if self.is_part:
            if isinstance(example_value, str):
                self.example_value = re.split(r'\n', example_value);
            else:
                self.example_value = None;

        self.entry = YamlEntry(depth=self.depth, key=self.label, multiline=self.is_part, value=self.example_value)
        pass;

    def __str__(self):
        return str(self.entry);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: YamlArguments
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class YamlArguments:
    entries: YamlEntries;

    def __init__(self, arguments: dict):
        self.entries = YamlEntries();
        for _ in arguments:
            for entry in YamlArguments.add_recursively(arguments[_], key=_, depth=0):
                self.entries.add(key=_, entry=entry);

    def __str__(self):
        return str(self.entries);

    @classmethod
    def add_recursively(cls, arguments, key: str, depth: int = 0):
        if not isinstance(arguments, dict):
            return;

        properties = Struct.get_value(arguments, 'properties');
        subproperties = Struct.get_value(arguments, 'subproperties');

        # yield entry, if properties are set:
        if isinstance(properties,dict):
            comment = Struct.get_value(properties, 'comment');
            value_type = Struct.get_value(properties, 'value-type');
            example_value = Struct.get_value(properties, 'example-value');
            if isinstance(value_type, str):
                value_type = string_to_type(value_type);
            if isinstance(comment, str) and not (value_type is None):
                comment = display_value_type(value_type) + ', ' + comment;
            yield YamlEntry(key=key, depth=depth, value=example_value, comment=comment);
        else:
            yield YamlEntry(key=key, depth=depth);

        # check if there are subproperties and yield these recursively:
        if isinstance(subproperties, dict):
            for _ in subproperties:
                yield from cls.add_recursively(subproperties[_], key=_, depth=depth+1);
        return;

