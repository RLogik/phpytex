#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;

from src.local.system import *;
from src.local.maths import *;
from src.local.typing import *;

from src.core.utils import PythonCommand;
from src.core.utils import getFullPath;
from src.customtypes.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_config_parameters: Dict[str, ConfigParameter] = {
    'pattern_config':          ConfigParameter[str]().setValue(r'^(|.*\.)(phpytex|phpycreate)\.(yml|yaml)$'),
    'path_app':                ConfigParameter[str](),
    'path_root':               ConfigParameter[str](),
    'file_start':              ConfigParameter[str](),
    'file_transpiled':         ConfigParameter[str](),
    'file_output':             ConfigParameter[str](),
    'file_stamp':              ConfigParameter[str](),
    'file_params_py':          ConfigParameter[str](),
    'import_param_py':         ConfigParameter[str](),
    'param_module_name':       ConfigParameter[str]().setValue('MODULE_GLOBAL_PARAMS'),
    'python_path':             ConfigParameter[str]().setValue(PythonCommand()),
    ####
    'option_legacy':           ConfigParameter[bool]().setValue(False),
    'option_ignore':           ConfigParameter[bool]().setValue(False),
    'option_debug':            ConfigParameter[bool]().setValue(False),
    'option_compile_latex':    ConfigParameter[bool]().setValue(False),
    'option_show_tree':        ConfigParameter[bool]().setValue(True),
    'option_comments':         ConfigParameter[str]().setValue('auto'),
    'option_insert_bib':       ConfigParameter[bool]().setValue(False),
    'option_overwrite_stamp':  ConfigParameter[bool]().setValue(True),
    'option_overwrite_params': ConfigParameter[bool]().setValue(True),
    'len_precode':             ConfigParameter[int]().setValue(0),
    'length_output':           ConfigParameter[int]().setValue(0),
    'max_length':              ConfigParameter[int]().setValue(10000),
        # <-- prevents transpiler from creating overlarge files
    'seed':                    ConfigParameter[int]().setValue(random.randint(0,10**8 - 1)),
    'indent_character':        ConfigParameter[str](),
    'indent_character_re':     ConfigParameter[str](),
    ####
    'has_error':               ConfigParameter[bool]().setValue(False),
    'has_py_error':            ConfigParameter[bool]().setValue(False),
    'is_too_long':             ConfigParameter[bool]().setValue(False),
    'censor_length':           ConfigParameter[int]().setValue(8),
};

_dictionary_stamp: Dict[str, Any] = dict();
_dictionary_params: Dict[str, Any] = dict();
_project_tree: ProjectTree = ProjectTree();
_export_vars:         Dict[str, Tuple[Any, str]] = dict();
_includes:            List[str] = [];
_precompile_lines:    List[Tuple[int, Any, str]] = [];
_document_structure:  List[str];
_list_of_imports:     List[str];

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

def getOptionComments() -> str:
    return _config_parameters['option_comments'].value;

def setOptionComments(value: str):
    global _config_parameters;
    _config_parameters['option_comments'].value = value;
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

def getLenPrecode() -> int:
    return _config_parameters['len_precode'].value;

def setLenPrecode(value: int):
    global _config_parameters;
    _config_parameters['len_precode'].value = value;
    return;

def getLengthOutput() -> int:
    return _config_parameters['length_output'].value;

def setLengthOutput(value: int):
    global _config_parameters;
    _config_parameters['length_output'].value = value;
    return;

def getMaxLengthOuput() -> int:
    return _config_parameters['max_length'].value;

def setMaxLengthOutput(value: int):
    global _config_parameters;
    _config_parameters['max_length'].value = value;
    return;

def getSeed() -> int:
    return _config_parameters['seed'].value;

def setSeed(value: int):
    global _config_parameters;
    _config_parameters['seed'].value = value;
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

def getHasError() -> bool:
    return _config_parameters['has_error'].value;

def setHasError(value: bool):
    global _config_parameters;
    _config_parameters['has_error'].value = value;
    return;

def getHasPyError() -> bool:
    return _config_parameters['has_py_error'].value;

def setHasPyError(value: bool):
    global _config_parameters;
    _config_parameters['has_py_error'].value = value;
    return;

def getIsTooLong() -> bool:
    return _config_parameters['is_too_long'].value;

def setIsTooLong(value: bool):
    global _config_parameters;
    _config_parameters['is_too_long'].value = value;
    return;

def getCensorLength() -> int:
    return _config_parameters['censor_length'].value;

def setCensorLength(value: int):
    global _config_parameters;
    _config_parameters['censor_length'].value = value;
    return;

def getDictionaryStamp() -> Dict[str, Any]:
    return _dictionary_stamp;

def setDictionaryStamp(value: Dict[str, Any]):
    global _dictionary_stamp;
    _dictionary_stamp = value;
    return;

def getDictionaryParms() -> Dict[str, Any]:
    return _dictionary_params;

def setDictionaryParams(value: Dict[str, Any]):
    global _dictionary_params;
    _dictionary_params = value;
    return;

def getProjectTree() -> ProjectTree:
    return _project_tree;

def setProjectTree(value: ProjectTree):
    global _project_tree;
    _project_tree = value;
    return;

def getExportVars() -> Dict[str, Tuple[Any, str]]:
    return _export_vars;

def setExportVars(value: Dict[str, Tuple[Any, str]]):
    global _export_vars;
    _export_vars = value;
    return;

def setExportVarsKeyValue(key: str, value: Any, codedvalue: str):
    global _export_vars;
    _export_vars[key] = (value, codedvalue);
    return;

def getIncludes() -> List[str]:
    return _includes;

def setIncludes(value: List[str]):
    global _includes;
    _includes = value;
    return;

def getPrecompileLines() -> List[Tuple[int, Any, str]]:
    return _precompile_lines;

def setPrecompileLines(value: List[Tuple[int, Any, str]]):
    global _precompile_lines;
    _precompile_lines = value;
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def relativisePath(path: str):
    return os.path.relpath(path=path, start=getPathRoot());
