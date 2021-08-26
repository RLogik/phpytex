#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

import re;
import random;
from typing import Any;
from typing import Dict;
from typing import List;
from typing import Tuple;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_file_pattern:        str = r'^.*\.phpycreate\.(yml|yaml)$';
_app_directory:       str;
_root_directory:      str;
_global_vars:         Dict[str, Any] = dict(__ROOT__='.', __DIR__='.');
_export_vars:         Dict[str, Any] = dict();
_includes:            List[str] = [];
_insert_bib:          bool = False;
_error:               bool = False;
_py_error:            bool = False;
_stamp_file:          str;
_phpytex_file:        str;
_script_file:         str;
_latex_file:          str;
_export_params:       bool = False;
_param_file:          str;
_param_py_import:     str;
_param_module_name:   str = 'MODULE_GLOBAL_PARAMS';
_len_precode:         int = 0;
_length_of_output:    int = 0;
_max_length:          int = 10000; # <-- prevents transpiler from creating overlarge files
_too_long:            bool = False;
# _seed:                int = random.getstate()[1][0];
_seed:                int = random.randint(0,10**8 - 1);
_precompile_lines:    List[Tuple[int, Any, str]] = [];
_censor_length:       int = 8;
_indent_character:    str;
_indent_character_re: str;
_document_structure:  List[str];
_list_of_imports:     List[str];
_indentation:         IndentationTracker;

# --------------------------------------------------------------------------------
# CLASS: indentation tracker
# --------------------------------------------------------------------------------

class IndentationTracker(object):
    pattern:   str;
    reference: int;
    start:     int;
    last:      int;

    def __init__(self, pattern: Any = None):
        self.pattern   = pattern if isinstance(pattern, str) else r'    ';
        self.reset();
        return;

    def reset(self):
        self.reference = 0;
        self.start     = 1;
        self.last      = 1;

    def computeIndentations(self, s: str, pattern = None) -> int:
        pattern = pattern if isinstance(pattern, str) else self.pattern;
        return len(re.findall(pattern, s));

    def initOffset(self, s: str):
        self.reset();
        self.reference = self.computeIndentations(s);

    def computeOffset(self, s: str):
        return max(self.computeIndentations(s) - self.reference, 1);

    def setOffset(self, s: str):
        self.last = self.computeOffset(s);

    def decrOffset(self):
        self.last = max(self.last - 1, 1);

    def incrOffset(self):
        self.last = self.last + 1;

## initialise
INDENTATION = IndentationTracker();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: get/set
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getFilePattern() -> str:
    return _file_pattern;

def setFilePattern(value: str):
    global _file_pattern;
    _file_pattern = value;
    return;

def getAppDirectory() -> str:
    return _app_directory;

def setAppDirectory(value: str):
    global _app_directory;
    _app_directory = value;
    return;

def getRootDirectory() -> str:
    return _root_directory;

def setRootDirectory(value: str):
    global _root_directory;
    _root_directory = value;
    return;

def getGlobalVars() -> Dict[str, Any]:
    return _global_vars;

def setGlobalVars(value: Dict[str, Any]):
    global _global_vars;
    _global_vars = value;
    return;

def getExportVars() -> Dict[str, Any]:
    return _export_vars;

def setExportVars(value: Dict[str, Any]):
    global _export_vars;
    _export_vars = value;
    return;

def getIncludes() -> List[str]:
    return _includes;

def setIncludes(value: List[str]):
    global _includes;
    _includes = value;
    return;

def getInsertBib() -> bool:
    return _insert_bib;

def setInsertBib(value: bool):
    global _insert_bib;
    _insert_bib = value;
    return;

def getError() -> bool:
    return _error;

def setError(value: bool):
    global _error;
    _error = value;
    return;

def getPyError() -> bool:
    return _py_error;

def setPyError(value: bool):
    global _py_error;
    _py_error = value;
    return;

def getStampFile() -> str:
    return _stamp_file;

def setStampFile(value: str):
    global _stamp_file;
    _stamp_file = value;
    return;

def getPhpytexFile() -> str:
    return _phpytex_file;

def setPhpytexFile(value: str):
    global _phpytex_file;
    _phpytex_file = value;
    return;

def getScriptFile() -> str:
    return _script_file;

def setScriptFile(value: str):
    global _script_file;
    _script_file = value;
    return;

def getLatexFile() -> str:
    return _latex_file;

def setLatexFile(value: str):
    global _latex_file;
    _latex_file = value;
    return;

def getExportParams() -> bool:
    return _export_params;

def setExportParams(value: bool):
    global _export_params;
    _export_params = value;
    return;

def getParamFile() -> str:
    return _param_file;

def setParamFile(value: str):
    global _param_file;
    _param_file = value;
    return;

def getParamPyImport() -> str:
    return _param_py_import;

def setParamPyImport(value: str):
    global _param_py_import;
    _param_py_import = value;
    return;

def getParamModuleName() -> str:
    return _param_module_name;

def setParamModuleName(value: str):
    global _param_module_name;
    _param_module_name = value;
    return;

def getLenPrecode() -> int:
    return _len_precode;

def setLenPrecode(value: int):
    global _len_precode;
    _len_precode = value;
    return;

def getLengthOfOutput() -> int:
    return _length_of_output;

def setLengthOfOutput(value: int):
    global _length_of_output;
    _length_of_output = value;
    return;

def getMaxLength() -> int:
    return _max_length;

def setMaxLength(value: int):
    global _max_length;
    _max_length = value;
    return;

def getTooLong() -> bool:
    return _too_long;

def setTooLong(value: bool):
    global _too_long;
    _too_long = value;
    return;

def getSeed() -> int:
    return _seed;

def setSeed(value: int):
    global _seed;
    _seed = value;
    return;

def getPrecompileLines() -> List[Tuple[int, Any, str]]:
    return _precompile_lines;

def setPrecompileLines(value: List[Tuple[int, Any, str]]):
    global _precompile_lines;
    _precompile_lines = value;
    return;

def getCensorLength() -> int:
    return _censor_length;

def setCensorLength(value: int):
    global _censor_length;
    _censor_length = value;
    return;

def getIndentCharacter() -> str:
    return _indent_character;

def setIndentCharacter(value: str):
    global _indent_character;
    _indent_character = value;
    return;

def getIndentCharacterRe() -> str:
    return _indent_character_re;

def setIndentCharacterRe(value: str):
    global _indent_character_re;
    _indent_character_re = value;
    return;

def getDocumentStructure() -> List[str]:
    return _document_structure;

def setDocumentStructure(value: List[str]):
    global _document_structure;
    _document_structure = value;
    return;

def getListOfImports() -> List[str]:
    return _list_of_imports;

def setListOfImports(value: List[str]):
    global _list_of_imports;
    _list_of_imports = value;
    return;

def getIndentation() -> IndentationTracker:
    return _indentation;

def initIndentation(pattern: Any = None):
    global _indentation;
    _indentation = IndentationTracker(pattern=pattern);
    return;

def setIndentation(value: IndentationTracker):
    global _indentation;
    _indentation = value;
    return;
