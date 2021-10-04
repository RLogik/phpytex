#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.misc import *;
from src.local.system import *;
from src.local.typing import *;

from src.core.log import *;
from src.core.utils import createNewFileName;
from src.core.utils import createNewPathName;
from src.core.utils import getAttribute;
from src.core.utils import getFilesByPattern;
from src.core.utils import readYamlFile;
from src.core.utils import restrictDictionary;
from src.core.utils import toPythonKeysDict;
from src.customtypes.exports import ProjectTree;
from src.setup import appconfig;
from src.setup.methods import extractPath;
from src.setup.userconfig import setupYamlReader;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step get config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step(fname: str):
    logInfo('READ CONFIG STARTED');
    ## get configuration file
    config = getPhpytexConfig(fname);
    ## get main parts of config
    config_compile = getAttribute(config, 'compile', 'options', expectedtype=dict, default=None) \
                     or getAttribute(config, 'compile', expectedtype=dict, default={});
    config_compile = preProcessCompileConfig(restrictDictionary(config, ['ignore']) | config_compile);
    config_stamp = getAttribute(config, 'stamp', expectedtype=dict, default={});
    config_parameters = getAttribute(config, 'parameters', expectedtype=dict, default={});

    ## set app config
    setCompileConfig(**config_compile);
    setStampConfig(**toPythonKeysDict(config_stamp));
    setParamsConfig(**toPythonKeysDict(config_parameters));
    setConfigFilesAndFolders(**toPythonKeysDict(config));

    assert not (appconfig.getFilePhpytex() == appconfig.getFileLatex()), 'The output and root files must be different!';
    logInfo('READ CONFIG COMPLETE');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getPhpytexConfig(fname: str) -> Dict[str, Any]:
    setupYamlReader();
    try:
        fname = fname or getFilesByPattern(path=appconfig.getPathRoot(), filepattern=appconfig.getPatternConfig())[0];
    except:
        raise Exception('Could not find or read any phpytex configuration files.');
    return readYamlFile(fname);

def preProcessCompileConfig(config: Dict[str, Any]) -> Dict[str, Any]:
    return dict(
        root       = getAttribute(config, 'root', expectedtype=str),
        seed       = getAttribute(config, 'seed', expectedtype=int),
        ignore     = getAttribute(config, 'ignore', expectedtype=bool, default=False),
        debug      = getAttribute(config, 'debug', expectedtype=bool, default=False),
        compile    = getAttribute(config, ['compile-latex', 'compile'], expectedtype=bool, default=False),
        insert_bib = getAttribute(config, 'insert-bib', expectedtype=bool, default=True),
        legacy     = getAttribute(config, 'legacy', expectedtype=bool, default=False),
        comments   = getAttribute(config, 'comments', expectedtype=str, default='auto'),
        show_tree  = getAttribute(config, ['show-structure', 'show-tree'], expectedtype=bool, default=True),
        max_length = getAttribute(config, 'max-length', expectedtype=int, default=10000),
        tabs       = getAttribute(config, 'tabs', expectedtype=bool, default=False),
        spaces     = getAttribute(config, 'spaces', expectedtype=int, default=4),
        output     = getAttribute(config, 'output', expectedtype=str, default='main.tex'),
    );

def setCompileConfig(
    # DEV-NOTE: This is the _only_ place that root refers to a file.
    # Otherwise root denotes the root directory in which the script is called.
    root:       str,
    seed:       int,
    ignore:     bool,
    debug:      bool,
    compile:    bool,
    insert_bib: bool,
    legacy:     bool,
    comments:   str,
    show_tree:  bool,
    max_length: int,
    tabs:       bool,
    spaces:     int,
    output:     str,
):
    appconfig.setOptionLegacy(legacy);
    appconfig.setOptionIgnore(ignore);
    appconfig.setOptionDebug(debug);
    appconfig.setOptionCompileLatex(compile);
    appconfig.setOptionInsertBib(insert_bib);
    appconfig.setOptionShowTree(show_tree);
    appconfig.setOptionComments(comments);
    appconfig.setSeed(seed);

    appconfig.setMaxLengthOutput(max_length);
    if tabs:
        appconfig.setIndentCharacter('\t');
        appconfig.setIndentCharacterRe(r'\t');
    else:
        appconfig.setIndentCharacter(' '*spaces);
        appconfig.setIndentCharacterRe(' '*spaces);

    appconfig.setFilePhpytex(setFile(root));
    appconfig.setFileLatex(setFile(output));

    root = appconfig.getPathRoot();
    file = createNewFileName(dir=root, nameinit='phpytex_main.py', namescheme='phpytex_main_{}.py');
    file = os.path.relpath(path=file, start=root);
    appconfig.setFileScript(setFile(file));
    return;

def setStampConfig(
    file: str = '',
    overwrite: bool = True,
    options: Dict[str, Any] = dict()
):
    root = appconfig.getPathRoot();
    if not isinstance(file, str) or file == '':
        file = createNewPathName(dir=root, nameinit='stamp.tex', namescheme='stamp_{}.tex');
        file = os.path.relpath(path=file, start=root);
    appconfig.setFileStamp(setFile(file));
    appconfig.setOptionOverwriteStamp(overwrite);
    appconfig.setDictionaryStamp(options);
    return;

def setParamsConfig(
    file: str = '',
    overwrite: bool = True,
    options: Dict[str, Any] = dict(),
):
    appconfig.setOptionOverwriteParams(overwrite);
    appconfig.setDictionaryParams(options);

    root = appconfig.getPathRoot();
    modulename = file if isinstance(file, str) else '';
    if re.match(r'^[^\.\s]*(\.[^\.\s]*)+$', file):
        path = re.sub(r'([^\.]+)\.', r'\1/', file) + '.py';
    else:
        logWarn('\033[1mparameters > file\033[0m option must by a python-like import path (relative to the root of the project).');
        path = createNewPathName(dir=root, nameinit='parameters.py', namescheme='parameters_{}.py');
        path = os.path.relpath(path, root);
    modulename = re.sub(r'\/', '.', os.path.splitext(path)[0]);

    appconfig.setImportParamsPy(modulename);
    appconfig.setFileParamsPy(setFile(path));
    return;

def setConfigFilesAndFolders(**config):
    appconfig.setProjectTree(ProjectTree(**config));
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TERTIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def setFile(file: str) -> str:
    return extractPath(path=file, relative=True);
