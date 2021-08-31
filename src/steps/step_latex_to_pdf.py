#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.core.log import logInfo;
from src.core.utils import pipeCall;
from src.setup import appconfig;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step compile latex to pdf
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step():
    # pipeCall('pdflatex', appconfig.getLatexFile(), errormsg='Pdflatex encountered a problem.');
    logInfo('Compilation (latex -> pdf) complete.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# try:
#     with open(____filetex_name____, 'w+') as ____filetex____:
#         ____compilephpytex();
#     if ____compilelatex____:
#         ____compilelatex();
#     else:
#         print('\nPDFLATEX WIRD NICHT AUSGEFÜHRT.');
#     ____cleanlatex();
# except Exception as e:
#     ## Provide information, then exit with status 1.
#     print("-----------------------------------------------------------------");
#     print("!!! (PH(p)y)TeX Compile error !!!");
#     if ____error_eval____:
#         ____last_latex____ = eval("'"+____last_latex____+"'");
#         print("  FILE: "+str(__FNAME__));
#         print("  LINE: "+str(__LINENR__ + 1)+" (local position in file).");
#         print("!!! Line could not be evaluated !!!");
#         print("-----------------------------------------------------------------");
#         print(____last_latex____);
#         print("-----------------------------------------------------------------");
#         ____forceprint("-----------------------------------------------------------------");
#         ____forceprint("!!! (PH(p)y)TeX Compile error !!!");
#         ____forceprint("  FILE: "+str(__FNAME__));
#         ____forceprint("  LINE: "+str(__LINENR__ + 1)+" (local position in file).");
#         ____forceprint("!!! Line could not be evaluated !!!");
#         ____forceprint("-----------------------------------------------------------------");
#         ____forceprint(____last_latex____);
#         ____forceprint("-----------------------------------------------------------------");
#     else:
#         print("-----------------------------------------------------------------");
#         # print(sys.exc_info());
#         print(e);
#         print("-----------------------------------------------------------------");
#     exit(1);
