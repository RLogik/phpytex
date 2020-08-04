#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from typing import Any;
from typing import Dict;

from .make import Make;
from .yamlentries import YamlEntries;
from ...core.logger import LoggerService;
from ...info.arguments import ArgumentValues;
from ...info.information import InformationService;
from ...values.struct import Struct;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INFO: InformationService;
LOG: LoggerService;
MODULENAME: str = 'example';
CONFIG: Struct;
WORKINGDIRECTORY: str;
MAKE: Make;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(info: InformationService, log: LoggerService, config: Struct, argumentValues: ArgumentValues):
    global INFO;
    global LOG;
    global CONFIG;
    global WORKINGDIRECTORY;
    global MAKE;
    global MODULENAME;

    INFO = info;
    LOG = log;
    CONFIG = config;
    WORKINGDIRECTORY = os.getcwd();

    subprog = argumentValues.getValueAsString('subprogramme');
    createexamples = extract_examples(subprog);
    MAKE = Make(createexamples);
    display_examples();
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def extract_examples(subprog: str) -> dict:
    global INFO;

    createexamples = INFO.get_attributes('programmes', 'examples', 'parts', subprog);

    # force formatting:
    if not isinstance(createexamples, dict):
        createexamples = dict();

    if subprog == 'create':
        # first extract the latest definitions for the transpile subprogramme:
        transpilearguments = dict();
        for label, argument in INFO.parse_arguments('transpile'):
            if not argument.create_example:
                continue;
            transpilearguments[label] = dict(
                properties={
                    'labels': argument.labels,
                    'example-value': argument.example_value,
                    'value-type': argument.value_type if argument.takes_value else None,
                    'comment': argument.comment,
                },
            );

        # now loop through all suitable examples and add example-value if missing.
        for key in createexamples:
            entry = Struct.get_value(createexamples[key], 'transpile', 'subproperties', 'options');
            if isinstance(entry, dict) and not ('subproperties' in entry):
                createexamples[key]['transpile']['subproperties']['options']['subproperties'] = transpilearguments;

    return createexamples;

def display_examples():
    global MAKE;
    global LOG;

    createexample = MAKE.get_createexample();
    example = Make.create_example(createexample);
    LOG.plain(str(example));
    return;
