#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from .yamlarguments import YamlArguments;
from ...info.arguments import Arguments;
from ...values.struct import Struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Make
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Make:
    createexamples: dict;

    def __init__(self, createexamples: dict):
        self.createexamples = createexamples;
        pass;

    def get_createexample(self, label=None) -> dict:
        if isinstance(label, str):
            createexample = Struct.get_value(self.createexamples, label, default=None);
        else:
            createexample = None;
            for _ in self.createexamples:
                createexample = Struct.get_value(self.createexamples, _, default=None);
                if not createexample is None:
                    break;
            if not isinstance(createexample, dict):
                raise AttributeError('No examples could be found in the configuration file.');
        return createexample;

    @staticmethod
    def create_example(createexample: dict) -> YamlArguments:
        return YamlArguments(createexample);
