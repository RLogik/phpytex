#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAKETE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import re;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_version(path: str) -> str:
    version = None;
    try:
        with open(os.path.join(path, 'VERSION')) as fp:
            for line in fp.readlines():
                line = re.sub(r'^[\s\n\r]+|[\s\n\r]+$', r'', line);
                if not re.match(r'^\d+\.\d+\.\d+$', line):
                    continue;
                version = line;
                break;
        if version is None:
            raise ValueError('Value in VERSION file is invalid!');
    except:
        raise FileNotFoundError('VERSION file missing in the distribution folder or could not be opened in read mode!');
    return version;