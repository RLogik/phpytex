#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.config import *;
from src.local.misc import *;
from src.local.system import *;
from src.local.typing import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOCAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

T = TypeVar('T')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD os sensitive commands
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def isLinux() -> bool:
    # return not ( os.name == 'nt' );
    return not ( platform.system().lower() == 'windows' );

def PythonCommand() -> str:
    return 'python3' if isLinux() else 'py -3';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: io
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## NOTE: subprocess.run is like subprocess.Popen but waits for result
def pipeCall(*args: str, cwd = None, errormsg: str = '', fnameOut: Union[None, str] = None):
    cwd = cwd if isinstance(cwd, str) else os.getcwd();
    if fnameOut is None:
        result = subprocess.run(list(args), cwd=cwd)
    else:
        with open(fnameOut, 'w') as fp:
            result = subprocess.run(list(args), cwd=cwd, stdout=fp);
    if result.returncode == 0:
        return;
    raise Exception(errormsg or 'Shell command < \033[94;1m{}\033[0m > failed.'.format(' '.join(args)));

def getFullPath(path: str, shouldexist: bool = False) -> str:
    path = os.path.abspath(path);
    if shouldexist and not os.path.exists(path):
        raise Exception('Path \033[1m{}\033[0m does not exist!');
    return path;

def formatPath(path: str, root: str, relative: bool, ext: Any = None, ext_if_empty: Any = None) -> str:
    if os.path.isabs(path):
        if relative:
            path = os.path.relpath(path=path, start=root);
    else:
        if not relative:
            path = os.path.abspath(os.path.join(root, path));
    path_, ext_ = os.path.splitext(path);
    if isinstance(ext, str):
        path = '{path}{ext}'.format(path=path_, ext=ext);
    elif isinstance(ext_if_empty, str) and ext_ == '':
        path = '{path}{ext}'.format(path=path_, ext=ext_if_empty);
    return path;

def getFiles(path: str) -> List[Tuple[str, str]]:
    items = [(_, os.path.join(path, _)) for _ in os.listdir(path)];
    return [ (_, __) for _, __ in items if os.path.isfile(__)];

def getFilesByPattern(path: str, filepattern: str) -> List[str]:
    regex = re.compile(filepattern);
    return [ __ for _, __ in getFiles(path) if regex.match(_) ];

def createNewPathName(dir: str, nameinit: str = 'tmp', namescheme: str = 'tmp_{}') -> str:
    path = os.path.join(dir, nameinit);
    i = 0;
    while os.path.isdir(path):
        path = os.path.join(dir, namescheme.format(i));
        i += 1;
    return path;

def createNewFileName(dir: str, nameinit: str = 'tmp', namescheme: str = 'tmp_{}') -> str:
    path = os.path.join(dir, nameinit);
    i = 0;
    while os.path.isfile(path):
        path = os.path.join(dir, namescheme.format(i));
        i += 1;
    return path;

def createPath(path: str):
    if path in [ '', '.', os.getcwd() ]:
        return;
    if not os.path.exists(path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True);
    if not os.path.exists(path):
        raise FileExistsError('Could not create or find path \033[93;1m{}\033[0m!'.format(path));
    return;

def createFile(path: str):
    if not os.path.exists(path):
        pathlib.Path(path).touch(exist_ok=True);
    if not os.path.exists(path):
        raise FileExistsError('Could not create or find path \033[93;1m{}\033[0m!'.format(path));
    return;

def readTextFile(path: str) -> str:
    with open(path, 'r') as fp:
        return ''.join(fp.readlines());

def writeTextFile(
    path: str,
    lines: Union[str, List[str]],
    force_create_path: bool = False,
    force_create_empty_line: bool = True
):
    if force_create_path:
        createPath(os.path.dirname(path));
    _lines = [ lines ] if isinstance(lines, str) else lines;
    while len(_lines) > 0:
        if not re.match(r'^\s*$', _lines[-1]):
            break;
        _lines = _lines[:-1];
    if force_create_empty_line:
        _lines = _lines + [''];
    with open(path, 'w') as fp:
        fp.write('\n'.join(_lines));
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: cli
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getCliArgs(*args: str) -> Tuple[List[str], Dict[str, Any]]:
    tokens = [];
    kwargs = {};
    N = len(args);
    indexes = [ i for i, arg in enumerate(args) if re.match(r'^\-+', arg) ];
    notindexes = [ i for i, _ in enumerate(args) if not (i in indexes) ];
    i = 0;
    while i < N:
        if i in indexes and i+1 in notindexes:
            key = re.sub(r'^\-*', '', args[i]).lower();
            value = args[i+1];
            kwargs[key] = value;
            i += 2;
            continue;
        m = re.match(r'^-*(.*?)\=(.*)$', args[i]);
        if m:
            key = re.sub(r'^\-*', '', m.group(1)).lower();
            value = m.group(2);
            kwargs[key] = value;
        else:
            arg = re.sub(r'^\-*', '', args[i]).lower();
            tokens.append(arg);
        i += 1;
    return tokens, kwargs;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: string
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# escapes string for use in python code
def escapeForPython(s: str, withformatting: bool = False) -> str:
    s = re.sub(r'(\\+)', r'\1\1', s);
    s = re.sub(r'\n', r'\\n', s);
    s = re.sub(r'\t', r'\\t', s);
    s = re.sub(r'\"', r'\\u0022', s);
    s = re.sub(r'\'', r'\\u0027', s);
    # s = re.sub(r'\%', slash+'u0025', s);
    if withformatting:
        s = re.sub(r'(\{+)', r'\1\1', s);
        s = re.sub(r'(\}+)', r'\1\1', s);
    return s;

## NOTE: dedent ignores lines that consist entirely of whitespaces, otherwise would needs to be handled differently:
def dedentIgnoreEmptyLines(s: str) -> str:
    return dedent(s);

def dedentRelativeTo(s: str, reference: str) -> str:
    lines = formatBlockUnindent(lines=s.split('\n'), reference=reference);
    return '\n'.join(lines);

def dedentIgnoreFirstAndLast(s: str) -> str:
    s = re.sub(r'^\s*[\n\r]|[\n\r]\s*$', '', s);
    return dedentIgnoreEmptyLines(s);

def formatBlockUnindent(lines: List[str], reference: str) -> List[str]:
    s = dedentIgnoreEmptyLines('\n'.join([ reference + '.' ] + lines));
    return s.split('\n')[1:];

def formatBlockIndent(lines: List[str], indent: str, unindent: bool = True) -> List[str]:
    if unindent:
        s = dedentIgnoreEmptyLines('\n'.join(lines));
        lines = s.split('\n');
    return [ indent + line for line in lines ];

def formatTextBlock(s: str) -> str:
    return dedentIgnoreFirstAndLast(s);

def formatTextBlockAsList(s: str, unindent: bool = True) -> List[str]:
    return re.split(r'\n', dedentIgnoreFirstAndLast(s) if unindent else s);

def extractIndent(s: str) -> str:
    return re.sub(r'^(\s*).*$', r'\1', s);

def lengthOfWhiteSpace(s: str) -> int:
    chars = [ _ for _ in re.split(r'', s) if not (_ == '') ];
    n = 0;
    for char in chars:
        if char == ' ':
            n += 1;
        elif char == '\t':
            n = (n - n % 8) + 8; # next tab stop
    return n;

def sizeOfIndent(s: str, indentsymb: str) -> int:
    lenIndent = lengthOfWhiteSpace(s);
    lenUnit = lengthOfWhiteSpace(indentsymb);
    return int(lenIndent / lenUnit);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: array methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def unique(X: List[Any]) -> List[Any]:
    X_ = [];
    for el in X:
        if el in X_:
            continue;
        X_.append(el);
    return X_;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: inheritance properties on graphs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def inheritanceOnGraph(edges: List[Tuple[str, str]], hasProperty: Dict[str, bool]):
    '''
    @inputs:
    - `edges` of a finite graph
    - an abstract `hasProperty` dictionary, assigning to each node, if property holds

    @returns:
    copy of `hasProperty` wherein all descendants of nodes with property have property
    '''
    P = [];
    for u, value in hasProperty.items():
        if value:
            P.append(u)
    properties = { u: value for u, value in hasProperty.items() };
    for u, v in edges:
        if not (u in properties):
            properties[u] = False;
        if not (v in properties):
            properties[v] = False;
    # keep updating until stable:
    while True:
        changed = False;
        for u, v in edges:
            if u in P and not (v in P):
                P.append(v);
                properties[v] = True;
                changed = True;
        if not changed:
            break;
    return properties;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: yaml and config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def readYamlFile(path: str) -> dict:
    with open(path, 'r') as fp:
        spec = yaml.load(fp, Loader=yaml.FullLoader);
        if not isinstance(spec, dict):
            raise ValueError('Config is not a dictionary object!');
    return spec;

def restrictDictionary(x: Dict[str, Any], keys: List[str]) -> dict:
    return { key: value for key, value in x.items() if key in keys };

def toPythonKeys(key: str) -> str:
    return re.sub(r'-', r'_', key);

def toPythonKeysDict(
    obj: T,
    deep: bool = False
) -> T:
    if deep:
        if isinstance(obj, dict):
            obj = { toPythonKeys(key): toPythonKeysDict(x, deep=True)
                    for key, x in obj.items() };
        elif isinstance(obj, list):
            obj = [ toPythonKeysDict(x, deep=True) for x in obj ];
    else:
        if isinstance(obj, dict):
            obj = { toPythonKeys(key): x for key, x in obj.items() };
    return obj

def getAttributeIgnoreError(obj: Any, *keys: Union[str, int], expectedtype: Union[Type, Tuple[Type]] = Any, default: Any = None):
    try:
        value = getAttribute(obj, *keys, expectedtype=expectedtype, default=default);
    except:
        value = default;
    return value;

def getAttribute(obj: Any, *keys: Union[str, int, List[Union[str, int]]], expectedtype: Union[Type, Tuple[Type]] = Any, default: Any = None) -> Any:
    if len(keys) == 0:
        return obj;
    nextkey = keys[0];
    nextkey = nextkey if isinstance(nextkey, list) else [ nextkey ];
    try:
        for key in nextkey:
            if isinstance(key, str) and isinstance(obj, dict) and key in obj:
                value = obj[key];
                if len(keys) <= 1:
                    return value if isinstance(value, expectedtype) else default;
                else:
                    return getAttribute(obj[key], *keys[1:], expectedtype=expectedtype, default=default);
            elif isinstance(key, int) and isinstance(obj, (list,tuple)) and key < len(obj):
                value = obj[key];
                if len(keys) <= 1:
                    return value if isinstance(value, expectedtype) else default;
                else:
                    return getAttribute(obj[key], *keys[1:], expectedtype=expectedtype, default=default);
    except:
        pass;
    if len(keys) <= 1:
        return default;
    path = ' -> '.join([ str(key) for key in keys ]);
    raise Exception('Could not find \033[1m{}\033[0m in object!'.format(path));
