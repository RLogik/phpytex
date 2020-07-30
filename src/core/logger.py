#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR:   rbitlogik@gmail.com / GitHub: RLogik
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
import logging as standard_logging;
from typing import Any;
from typing import Union;

from .config import transfer_config;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Auxilary class: LoggerConfig
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@transfer_config
class LoggerConfig(dict):
    stdout: bool = True;
    name: str = 'root';
    directory: str = '.';
    file: str = 'basic.log';
    mode: str = 'a';
    format: str = '%(name)s | %(levelname)s | %(message)s';
    dateformat: str = '%Y-%m-%d %H:%M:%S';
    level: str = 'DEBUG';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class: Logger
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Logger():
    __config: LoggerConfig;
    __LOGGER = None;
    __is_set = False;

    def __init__(self, config):
        self.__config = LoggerConfig(**config);
        self.__initialise();
        return;

    ################################################################
    ################################
    ## START OF PROPERTIES
    @property
    def isSet(self):
        return self.__is_set;

    @isSet.setter
    def isSet(self, x: bool):
        self.__is_set = x;

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
    def dateformat(self) -> str:
        fmt = self.__config.dateformat;
        return fmt.encode().decode('unicode-escape');

    @property
    def level(self) -> Any:
        key = self.__config.level;
        return standard_logging.getLevelName(key);

    @property
    def getLogger(self) -> Any:
        return self.__LOGGER;

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
    ## START OF CONFIGURATION
    def __initialise(self):
        try:
            self.__close();
            standard_logging.basicConfig(
                format=self.format,
                datefmt=self.dateformat,
                filename=self.fileNameWithPath,
                filemode=self.filemode,
                level=self.level
            );
            self.__LOGGER = standard_logging.getLogger(self.entryname);
            self.isSet = True;
        except:
            self.__close();
        return self.isSet;

    def __close(self):
        if self.isSet and not self.__LOGGER is None:
            del self.__LOGGER;
        self.isSet = False;
        self.__LOGGER = None;
        return;
    ## END OF CONFIGURATION
    ################################
    ################################################################

    ################################################################
    ################################
    ## START OF MAIN METHODS
    def plain(self, *messages: str):
        print(*messages);
        return True;

    def info(self, message: str):
        if not self.isSet:
            return False;
        try:
            self.__LOGGER.info(message);
            return True;
        except:
            return False;

    def debug(self, message: str):
        if not self.isSet:
            return False;
        try:
            self.__LOGGER.debug(message);
            return True;
        except:
            return False;

    def warning(self, message: str):
        if not self.isSet:
            return False;
        try:
            self.__LOGGER.warning(message);
            return True;
        except:
            return False;

    def error(self, message: str):
        if not self.isSet:
            return False;
        try:
            self.__LOGGER.error(message);
            return True;
        except:
            return False;

    def critical(self, message: str):
        if not self.isSet:
            return False;
        try:
            self.__LOGGER.critical(message);
            return True;
        except:
            return False;
    ## END OF MAIN METHODS
    ################################
    ################################################################
    pass;
