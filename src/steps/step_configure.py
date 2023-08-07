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
from src.core.utils import formatPath;
from src.core.utils import getAttribute;
from src.core.utils import getFilesByPattern;
from src.core.utils import lengthOfWhiteSpace;
from src.core.utils import readYamlFile;
from src.core.utils import restrictDictionary;
from src.core.utils import toPythonKeysDict;
from src.customtypes.exports import ProjectTree;
from src.setup import appconfig;
from src.setup.userconfig import setupYamlReader;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step get config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step(fnameConfig: str, extra_parameters: dict):
    logInfo('READ CONFIG STARTED');
    ## get configuration file
    config = getPhpytexConfig(fnameConfig);
    ## get main parts of config
    config_compile = getAttribute(config, 'compile', 'options', expectedtype=dict, default=None) \
                     or getAttribute(config, 'compile', expectedtype=dict, default={});
    config_compile = preProcessCompileConfig({ **restrictDictionary(config, ['ignore']), **config_compile });
    config_stamp = getAttribute(config, 'stamp', expectedtype=dict, default={});
    config_parameters: dict = getAttribute(config, 'parameters', expectedtype=dict, default={});
    config_parameters['options'] = {**config_parameters.get('options', {}), **extra_parameters};

    ## set app config
    setCompileConfig(**config_compile);
    setStampConfig(**toPythonKeysDict(config_stamp));
    setParamsConfig(**toPythonKeysDict(config_parameters));
    setConfigFilesAndFolders(toPythonKeysDict(config));

    logInfo('READ CONFIG COMPLETE');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getPhpytexConfig(fnameConfig: str) -> Dict[str, Any]:
    setupYamlReader();
    try:
        if not isinstance(fnameConfig, str) or fnameConfig == '':
            fnameConfig = getFilesByPattern(
                path        = appconfig.getPathRoot(),
                filepattern = appconfig.getPatternConfig()
            )[0];
    except:
        raise Exception('Could not find or read any phpytex configuration files.');
    return readYamlFile(fnameConfig);

def preProcessCompileConfig(config: Dict[str, Any]) -> Dict[str, Any]:
    return dict(
        ignore     = getAttribute(config, 'ignore', expectedtype=bool, default=False),
        legacy     = getAttribute(config, 'legacy', expectedtype=bool, default=False),
        startfile  = getAttribute(config, ['root', 'input'], expectedtype=str),
        outputfile = getAttribute(config, 'output', expectedtype=str, default='main.tex'),
        debug      = getAttribute(config, 'debug', expectedtype=bool, default=False),
        compile    = getAttribute(config, ['compile-latex', 'compile'], expectedtype=bool, default=False),
        insert_bib = getAttribute(config, 'insert-bib', expectedtype=bool, default=True),
        backend_bib = getAttribute(config, 'backend-bib', expectedtype=str, default='bibtex'),
        comments   = getAttribute(config, 'comments', expectedtype=(str,bool), default='auto'),
        show_tree  = getAttribute(config, ['show-structure', 'show-tree'], expectedtype=bool, default=False),
        max_length = getAttribute(config, 'max-length', expectedtype=int, default=10000),
        tabs       = getAttribute(config, 'tabs', expectedtype=bool, default=False),
        spaces     = getAttribute(config, 'spaces', expectedtype=int, default=4),
        ## NOTE: Do not force seed to be set if not given. Allow user to decide to NOT seed the rng.
        seed       = getAttribute(config, 'seed', expectedtype=int, default=None),
        offset     = getAttribute(config, 'offset', expectedtype=str, default=''),
        align      = getAttribute(config, 'align', expectedtype=bool, default=True),
    );

def setCompileConfig(
    ignore:     bool,
    legacy:     bool,
    startfile:  str,
    outputfile: str,
    debug:      bool,
    compile:    bool,
    insert_bib: bool,
    backend_bib: str,
    comments:   Union[str, bool],
    show_tree:  bool,
    max_length: int,
    tabs:       bool,
    spaces:     int,
    seed:       Any,
    offset:     str,
    align:      bool,
):
    root = appconfig.getPathRoot();
    appconfig.setOptionLegacy(legacy);
    appconfig.setOptionIgnore(ignore);
    appconfig.setOptionDebug(debug);
    appconfig.setOptionCompileLatex(compile);
    appconfig.setOptionInsertBib(insert_bib);
    appconfig.setOptionBackendBib(backend_bib);
    appconfig.setOptionShowTree(show_tree);
    if isinstance(comments, str):
        appconfig.setOptionCommentsAuto(comments in [ 'auto', 'default' ]);
        appconfig.setOptionCommentsOn(comments in [ 'on', 'default' ] or not comments in [ 'off' ]);
    else:# elif isinstance(comments, bool):
        appconfig.setOptionCommentsAuto(False);
        appconfig.setOptionCommentsOn(comments);
    if isinstance(seed, int):
        appconfig.setSeed(seed);
    appconfig.setOffsetSymbol(offset);
    appconfig.setOptionAlign(align);

    appconfig.setMaxLengthOutput(max_length);
    if tabs:
        appconfig.setIndentCharacter('\t');
        appconfig.setIndentCharacterRe(r'\t');
    else:
        appconfig.setIndentCharacter(' '*spaces);
        appconfig.setIndentCharacterRe(' '*spaces);
    indentsymb = appconfig.getIndentCharacter();
    if lengthOfWhiteSpace(indentsymb) == 0:
        raise AttributeError('Indentation symbol cannot be the empty string!');
    if legacy:
        appconfig.setOffsetSymbol(indentsymb);

    fileStart = formatPath(startfile, root=root, relative=False);
    fileOutput = formatPath(outputfile, root=root, relative=False, ext_if_empty='.tex');

    assert os.path.dirname(fileOutput) == root, 'The output file can only be set to be in the root directory!';
    assert not (fileStart == fileOutput), 'The output and start (\'root\'-attribute in config) paths must be different!';

    appconfig.setFileStart(fileStart);
    appconfig.setFileOutput(fileOutput);

    # file = createNewFileName(dir=root, nameinit='phpytex_transpiled.py', namescheme='phpytex_transpiled_{}.py');
    file = 'phpytex_transpiled.py';
    appconfig.setFileTranspiled(formatPath(file, root=root, relative=False));
    return;

def setStampConfig(
    file: str = '',
    overwrite: bool = True,
    options: Dict[str, Any] = dict()
):
    root = appconfig.getPathRoot();
    if not isinstance(file, str) or file == '':
        file = 'stamp.tex';
        file = os.path.relpath(path=file, start=root);

    if not isinstance(options, dict) or len(options) == 0:
        appconfig.setWithFileStamp(False);
    else:
        appconfig.setWithFileStamp(True);
        appconfig.setFileStamp(formatPath(file, root=root, relative=False));
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
        path = 'parameters.py';
        path = os.path.relpath(path, root);
    modulename = re.sub(r'\/', '.', os.path.splitext(path)[0]);

    if not isinstance(options, dict) or len(options) == 0:
        appconfig.setWithFileParamsPy(False);
    else:
        appconfig.setWithFileParamsPy(True);
        appconfig.setImportParamsPy(modulename);
        appconfig.setFileParamsPy(formatPath(path, root=root, relative=False));
    return;

def setConfigFilesAndFolders(config: Dict[str, Any]):
    appconfig.setProjectTree(ProjectTree(**config));
    return;
