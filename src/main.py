#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))));

from src.thirdparty.config import *;

from src.setup import *;
from src.core.log import *;
from src.core.utils import getCliArgs;
from src.endpoints.exports import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_pattern_config: str = r'^(|.*\.)(phpytex|phpycreate)\.(yml|yaml)$';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN PROCESS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def enter(*tokens: str, file: str, pathApp: str, pathRoot: str, **kwargs: str):
    appconfig.setPathApp(pathApp);
    appconfig.setPathRoot(pathRoot);
    appconfig.setPatternConfig(_pattern_config);

    setQuietMode(('q' in tokens));
    if ('version' in tokens) or ('v' in tokens):
        endpoint_display_version();
    elif ('help' in tokens) or ('info' in tokens) or ('man' in tokens):
        endpoint_display_help();
    elif 'run' in tokens:
        parameters = {};
        if 'parameters' in kwargs:
            try:
                parameters = json.loads(kwargs['parameters']);
            except:
                pass;
        endpoint_run_phpytex(fnameConfig=file, parameters=parameters);
    else:
        endpoint_display_help();
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    sys.tracebacklimit = 0;
    open_source(True);
    tokens, kwargs = getCliArgs(*sys.argv[1:]);
    enter(*tokens, **{
        'file':     '',
        'pathApp':  os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'pathRoot': os.getcwd(),
        **kwargs
    });
