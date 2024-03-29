#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.core.utils import formatTextBlock;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENDPOINT display help
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def endpoint():
    print('');
    print(formatTextBlock(
        '''
        Usage of \033[32;1m(PH(p)y)tex\033[0m
        ~~~~~~~~~~~~~~~~~~~~

        - Version and help:

            phpytex \033[1mversion\033[0m
            phpytex \033[1mhelp\033[0m

        - To run the transpiler within a project, call one of:

            phpytex \033[1mrun\033[0m
            phpytex \033[1mrun\033[0m [\033[1mfile\033[0m=\033[2m<name of config file>\033[0m]

          If the optional flag is left empty, the programme searches for the first yaml-file
          in the directory which matches

            \033[1m*.(phpytex|phpycreate).(yml|yaml)\033[0m
        '''
    ));
    print('');
    return;
