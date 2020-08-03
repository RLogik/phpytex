#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR:   RLogik/GitHub
# CREATED:  4. April 2020
# FILE:     local_log.py
#
# NOTES:
# Methods can be found in
#   https://docs.python.org/3/howto/logging.html
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
from typing import Any;
from typing import Union;

from .utils import purify;
from ..values.configurable import Configurable
from ..values.configurable import transfer
from ..values.valuetypes import ValueType

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Auxilary class: LoggerConfig
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@transfer
class LoggerConfig(Configurable):
    _DEFAULT = dict(
        stdout     = ValueType(bool, True),
        name       = ValueType(str,  'root'),
        directory  = ValueType(str,  None),
        file       = ValueType(str,  None),
        mode       = ValueType(str,  'a'),
        format     = ValueType(str,  '%(name)s | %(levelname)s | %(message)s'),
        dateformat = ValueType(str,  '%Y-%m-%d %H:%M:%S'),
        level      = ValueType(str,  'DEBUG'),
        colourmode = ValueType(bool, True),
        verbose    = ValueType(bool, False),
    );

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Logger
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Logger:
    __config: LoggerConfig;

    def __init__(self, config):
        self.__config = LoggerConfig(**config);
        return;

    ################################################################
    ################################
    ## START OF PROPERTIES
    @property
    def datefmt(self) -> str:
        return self.__config.dateformat;

    @property
    def entryname(self) -> str:
        return self.__config.name;

    @property
    def path(self) -> Union[str, None]:
        try:
            relpath = self.__config.directory;
            return os.path.abspath(relpath);
        except:
            return None;

    @property
    def to_stdout(self) -> bool:
        return self.__config.stdout;

    @property
    def filename(self) -> str:
        return self.__config.file;

    @property
    def filemode(self) -> str:
        return self.__config.mode;

    @property
    def format(self) -> str:
        fmt = self.__config.format;
        return fmt.encode().decode('unicode-escape');

    @property
    def verbose(self) -> bool:
        return self.__config.verbose;

    @verbose.setter
    def verbose(self, x: bool):
        self.__config.verbose = x;

    @property
    def colourmode(self) -> bool:
        return self.to_stdout and self.__config.colourmode;

    @colourmode.setter
    def colourmode(self, x: bool):
        self.__config.colourmode = x;

    @property
    def dateformat(self) -> str:
        fmt = self.__config.dateformat;
        return fmt.encode().decode('unicode-escape');

    @property
    def level(self) -> Any:
        return self.__config.level;

    @property
    def fileNameWithPath(self) -> Union[str, None]:
        if self.to_stdout or self.path is None:
            return None;
        try:
            return os.path.join(self.path, self.filename);
        except:
            return None;
    ## END OF PROPERTIES
    ################################
    ################################################################

    ################################################################
    ################################
    ## START OF MAIN METHODS
    def plain(self, *messages: str):
        print(*[ self.optional_purify(msg) for msg in messages ], sep='\n');

    def __print(self, level: str, *messages: str):
        _messages = messages;
        if self.verbose:
            _messages = [self.format % dict(asctime='', name=self.entryname, levelname=level, message=msg) for msg in messages];
        self.plain(*_messages);

    def info(self, *messages: str):
        self.__print('INFO', *messages);

    def debug(self, *messages: str):
        self.__print('DEBUG', *messages);

    def warning(self, *messages: str):
        self.__print('WARNING', *messages);

    def error(self, *messages: str):
        self.__print('ERROR', *messages);

    def critical(self, *messages: str):
        self.__print('FATAL', *messages);

    # avoid using outside the classe, except for debugging
    def console(self, *messages: str, sep='\n'):
        print(*[self.optional_purify(msg) for msg in messages], sep=sep);
        return True;
    ## END OF MAIN METHODS
    ################################
    ################################################################

    ################################################################
    ################################
    ## START OF AUXILIARY METHODS
    def optional_purify(self, text: str) -> str:
        return text if self.colourmode else purify(text);
    ## END OF AUXILIARY METHODS
    ################################
    ################################################################
