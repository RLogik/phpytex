#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.thirdparty.system import *;
from src.thirdparty.maths import *;
from src.thirdparty.types import *;

from src.core.utils import PythonCommand;
from src.core.utils import getFullPath;
from src.customtypes.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_config_parameters: dict[str, ConfigParameter] = {
    'pattern_config':          ConfigParameter[str]('patternConfig'),
    'path_app':                ConfigParameter[str]('pathApp'),
    'path_root':               ConfigParameter[str]('pathRoot'),
    'file_start':              ConfigParameter[str]('fileStart'),
    'file_transpiled':         ConfigParameter[str]('fileTranspiled'),
    'file_output':             ConfigParameter[str]('fileOutput'),
    'file_stamp':              ConfigParameter[str]('fileStamp'),
    'with_file_stamp':         ConfigParameter[bool]('withFileStamp').setValue(False),
    'file_params_py':          ConfigParameter[str]('fileParamsPy'),
    'with_file_params_py':     ConfigParameter[bool]('withFileParamsPy').setValue(False),
    'import_param_py':         ConfigParameter[str]('importParamPy'),
    'param_module_name':       ConfigParameter[str]('paramModuleName').setValue('MODULE_GLOBAL_PARAMS'),
    'python_path':             ConfigParameter[str]('pythonPath').setValue(PythonCommand()),
    ####
    'option_legacy':           ConfigParameter[bool]('optionLegacy').setValue(False),
    'option_ignore':           ConfigParameter[bool]('optionIgnore').setValue(False),
    'option_debug':            ConfigParameter[bool]('optionDebug').setValue(False),
    'option_compile_latex':    ConfigParameter[bool]('optionCompileLatex').setValue(False),
    'option_show_tree':        ConfigParameter[bool]('optionShowTree').setValue(True),
    'option_comments_auto':    ConfigParameter[bool]('optionCommentsAuto').setValue(True),
    'option_comments_on':      ConfigParameter[bool]('optionCommentsOn').setValue(True),
    'option_insert_bib':       ConfigParameter[bool]('optionInsertBib').setValue(False),
    'option_overwrite_stamp':  ConfigParameter[bool]('optionOverwriteStamp').setValue(True),
    'option_overwrite_params': ConfigParameter[bool]('optionOverwriteParams').setValue(True),
    'max_length':              ConfigParameter[int]('maxLength').setValue(10000),
        # <-- prevents transpiler from creating overlarge files
    'seed':                    ConfigParameter[int]('seed'),
    'indent_character':        ConfigParameter[str]('indentCharacter'),
    'indent_character_re':     ConfigParameter[str]('indentCharacterRe'),
    'censor_symbol':           ConfigParameter[str]('censorSymbol').setValue('########'),
    'offset_symbol':           ConfigParameter[str]('offsetSymbol').setValue(''),
};

_dictionary_stamp: dict[str, Any] = dict();
_dictionary_params: dict[str, Any] = dict();
_project_tree: ProjectTree = ProjectTree();
_export_vars:         dict[str, tuple[Any, str]] = dict();
_includes:            list[str] = [];
_precompile_lines:    list[tuple[int, Any, str]] = [];
_document_structure:  list[str];
_list_of_imports:     list[str];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: get/set
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getPatternConfig() -> str:
    return _config_parameters['pattern_config'].value;

def setPatternConfig(value: str):
    global _config_parameters;
    _config_parameters['pattern_config'].value = value;
    return;

def getPathApp() -> str:
    return _config_parameters['path_app'].value;

def setPathApp(value: str):
    global _config_parameters;
    try:
        path = getFullPath(value or '.');
    except:
        raise Exception('Path \033[1m{}\033[0m does not exist and cannot be used as the app path!'.format(value));
    _config_parameters['path_app'].value = path;
    return;

def getPathRoot() -> str:
    return _config_parameters['path_root'].value;

def setPathRoot(value: str):
    global _config_parameters;
    try:
        path = getFullPath(value or '.');
        os.chdir(path);
    except:
        raise Exception('Path \033[1m{}\033[0m does not exist and cannot be used as the root path!'.format(value));
    _config_parameters['path_root'].value = value;
    return;

def getPythonPath() -> str:
    return _config_parameters['python_path'].value;

def setPythonPath(value: str):
    global _config_parameters;
    _config_parameters['python_path'].value = value;
    return;

def getOptionInsertBib() -> bool:
    return _config_parameters['option_insert_bib'].value;

def setOptionInsertBib(value: bool):
    global _config_parameters;
    _config_parameters['option_insert_bib'].value = value;
    return;

def getOptionOverwriteStamp() -> bool:
    return _config_parameters['option_overwrite_stamp'].value;

def setOptionOverwriteStamp(value: bool):
    global _config_parameters;
    _config_parameters['option_overwrite_stamp'].value = value;
    return;

def getOptionOverwriteParams() -> bool:
    return _config_parameters['option_overwrite_params'].value;

def setOptionOverwriteParams(value: bool):
    global _config_parameters;
    _config_parameters['option_overwrite_params'].value = value;
    return;

def getWithFileStamp() -> bool:
    return _config_parameters['with_file_stamp'].value;

def setWithFileStamp(value: bool):
    global _config_parameters;
    _config_parameters['with_file_stamp'].value = value;
    return;

def getFileStamp(rel: bool = True) -> str:
    path = os.path.abspath(_config_parameters['file_stamp'].value);
    return relativisePath(path) if rel else path;

def setFileStamp(value: str):
    global _config_parameters;
    if value == '':
        return;
    _config_parameters['file_stamp'].value = value;
    return;

def getFileStart(rel: bool = True) -> str:
    path = os.path.abspath(_config_parameters['file_start'].value);
    return relativisePath(path) if rel else path;

def setFileStart(value: str):
    global _config_parameters;
    if value == '':
        return;
    _config_parameters['file_start'].value = value;
    return;

def getFileTranspiled(rel: bool = True) -> str:
    path = os.path.abspath(_config_parameters['file_transpiled'].value);
    return relativisePath(path) if rel else path;

def setFileTranspiled(value: str):
    global _config_parameters;
    if value == '':
        return;
    _config_parameters['file_transpiled'].value = value;
    return;

def getFileOutput(rel: bool = True) -> str:
    path = os.path.abspath(_config_parameters['file_output'].value);
    return relativisePath(path) if rel else path;

def getFileOutput(rel: bool = True) -> str:
    path = os.path.abspath(_config_parameters['file_output'].value);
    return relativisePath(path) if rel else path;

def getFileOutputBase() -> str:
    path = _config_parameters['file_output'].value;
    return os.path.splitext(os.path.basename(path))[0];

def setFileOutput(value: str):
    global _config_parameters;
    if value == '':
        return;
    _config_parameters['file_output'].value = value;
    return;

def getOptionLegacy() -> bool:
    return _config_parameters['option_legacy'].value;

def setOptionLegacy(value: bool) -> bool:
    global _config_parameters;
    _config_parameters['option_legacy'].value = value;
    return;

def getOptionIgnore() -> bool:
    return _config_parameters['option_ignore'].value;

def setOptionIgnore(value: bool):
    global _config_parameters;
    _config_parameters['option_ignore'].value = value;
    return;

def getOptionDebug() -> bool:
    return _config_parameters['option_debug'].value;

def setOptionDebug(value: bool):
    global _config_parameters;
    _config_parameters['option_debug'].value = value;
    return;

def getOptionCompileLatex() -> bool:
    return _config_parameters['option_compile_latex'].value;

def setOptionCompileLatex(value: bool):
    global _config_parameters;
    _config_parameters['option_compile_latex'].value = value;
    return;

def getOptionShowTree() -> bool:
    return _config_parameters['option_show_tree'].value;

def setOptionShowTree(value: bool):
    global _config_parameters;
    _config_parameters['option_show_tree'].value = value;
    return;

def getOptionCommentsAuto() -> bool:
    return _config_parameters['option_comments_auto'].value;

def setOptionCommentsAuto(value: bool):
    global _config_parameters;
    _config_parameters['option_comments_auto'].value = value;
    return;

def getOptionCommentsOn() -> bool:
    return _config_parameters['option_comments_on'].value;

def setOptionCommentsOn(value: bool):
    global _config_parameters;
    _config_parameters['option_comments_on'].value = value;
    return;

def getWithFileParamsPy() -> bool:
    return _config_parameters['with_file_params_py'].value;

def setWithFileParamsPy(value: bool):
    global _config_parameters;
    _config_parameters['with_file_params_py'].value = value;
    return;

def getFileParamsPy(rel: bool = True) -> str:
    path = os.path.abspath(_config_parameters['file_params_py'].value);
    return relativisePath(path) if rel else path;

def setFileParamsPy(value: str):
    global _config_parameters;
    _config_parameters['file_params_py'].value = value;
    return;

def getImportParamsPy() -> str:
    return _config_parameters['import_param_py'].value;

def setImportParamsPy(value: str):
    global _config_parameters;
    _config_parameters['import_param_py'].value = value;
    return;

def getParamModuleName() -> str:
    return _config_parameters['param_module_name'].value;

def setParamModuleName(value: str):
    global _config_parameters;
    _config_parameters['param_module_name'].value = value;
    return;
    return;

def getMaxLengthOuput() -> int:
    return _config_parameters['max_length'].value;

def setMaxLengthOutput(value: int):
    global _config_parameters;
    _config_parameters['max_length'].value = value;
    return;

def hasSeed() -> bool:
    return _config_parameters['seed'].hasValue;

def getSeed() -> int:
    return _config_parameters['seed'].value;

def setSeed(value: int):
    global _config_parameters;
    _config_parameters['seed'].value = value;
    return;

def reSeed():
    global _config_parameters;
    if _config_parameters['seed'].hasValue:
        random.seed(_config_parameters['seed'].value);
    return;

def getIndentCharacter() -> str:
    return _config_parameters['indent_character'].value;

def setIndentCharacter(value: str):
    global _config_parameters;
    _config_parameters['indent_character'].value = value;
    return;

def getIndentCharacterRe() -> str:
    return _config_parameters['indent_character_re'].value;

def setIndentCharacterRe(value: str):
    global _config_parameters;
    _config_parameters['indent_character_re'].value = value;
    return;

def getCensorSymbol() -> str:
    return _config_parameters['censor_symbol'].value;

def setCensorSymbol(value: str):
    global _config_parameters;
    _config_parameters['censor_symbol'].value = value;
    return;

def getOffsetSymbol() -> str:
    return _config_parameters['offset_symbol'].value;

def setOffsetSymbol(value: str):
    global _config_parameters;
    _config_parameters['offset_symbol'].value = value;
    return;

def getDictionaryStamp() -> dict[str, Any]:
    return _dictionary_stamp;

def setDictionaryStamp(value: dict[str, Any]):
    global _dictionary_stamp;
    _dictionary_stamp = value;
    return;

def getDictionaryParms() -> dict[str, Any]:
    return _dictionary_params;

def setDictionaryParams(value: dict[str, Any]):
    global _dictionary_params;
    _dictionary_params = value;
    return;

def getProjectTree() -> ProjectTree:
    return _project_tree;

def setProjectTree(value: ProjectTree):
    global _project_tree;
    _project_tree = value;
    return;

def getExportVars() -> dict[str, tuple[Any, str]]:
    return _export_vars;

def setExportVars(value: dict[str, tuple[Any, str]]):
    global _export_vars;
    _export_vars = value;
    return;

def setExportVarsKeyValue(key: str, value: Any, codedvalue: str):
    global _export_vars;
    _export_vars[key] = (value, codedvalue);
    return;

def getIncludes() -> list[str]:
    return _includes;

def setIncludes(value: list[str]):
    global _includes;
    _includes = value;
    return;

def getPrecompileLines() -> list[tuple[int, Any, str]]:
    return _precompile_lines;

def setPrecompileLines(value: list[tuple[int, Any, str]]):
    global _precompile_lines;
    _precompile_lines = value;
    return;

def getDocumentStructure() -> list[str]:
    return _document_structure;

def setDocumentStructure(value: list[str]):
    global _document_structure;
    _document_structure = value;
    return;

def getListOfImports() -> list[str]:
    return _list_of_imports;

def setListOfImports(value: list[str]):
    global _list_of_imports;
    _list_of_imports = value;
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def relativisePath(path: str):
    return os.path.relpath(path=path, start=getPathRoot());
