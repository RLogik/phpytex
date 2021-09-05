#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.core.log import *;
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

# ## PDFLATEX:
# def ____compilelatex():
#     print('\n\nPDFLATEX WIRD AUSGEFÜHRT:');
#     outfile, _ = os.path.splitext(____filetex_name____);
#     # pipeCall('pdflatex', '-interaction=scrollmode', fnameOut=outfile);
#     # pipeCall('pdflatex', '-interaction=batchmode', fnameOut=outfile);
#     pipeCall('pdflatex', '-interaction=errorstopmode', fnameOut=outfile);
#     # pipeCall('pdflatex', '-interaction=nonstopmode', fnameOut=outfile);
#     print('\n\nBIBTEX WIRD AUSGEFÜHRT:');
#     for src in ____lines____['bib']:
#         src, _ = os.path.splitext(src);
#         pipeCall('bibtex', src);
#     print('\n\nDOKUMENT \033[1m{{fname}}.pdf\033[0m WURDE FERTIGGESTELLT.'.format(fname=____filetex_name_rel____));
#     pass;
#
# ## ERSETZUNG VON \bibliography-Befehlen durch Inhalte + Anonymisierung:
# def ____cleanlatex():
#     global ____filetex____;
#
#     with open(____filetex_name____, 'w+') as ____filetex____:
#         bibindex = [ ];
#         bibtext = {{}};
#         for src in ____lines____['bib']:
#             bibindex += ____lines____['bib'][src];
#             n = len(____lines____['bib'][src]);
#             biblines = [];
#             try:
#                 fp = open(src, 'r');
#                 lines = fp.readlines();
#                 fp.close();
#                 for bibline in lines:
#                     bibline = re.sub(r'[\s\n]+$', '', bibline);
#                     bibline = re.sub(r'^(.*)\%(.*)', r'\1', bibline);
#                     if re.match(r'^\s*\%.*', bibline):
#                         continue;
#                     biblines.append(bibline);
#                     pass;
#             except:
#                 biblines = None;
#                 print('Warning! Bib-file \033[1m{{fname}}\033[0m could not be found.'.format(fname=src));
#             bibtext[src] = biblines;
#             pass;

#         nr_lines = len(____lines____['post-compile']);
#         for n, line in enumerate(____lines____['post-compile']):
#             if n in ____lines____['anon']:
#                 continue;
#             if n in bibindex:
#                 src = None
#                 for src_ in ____lines____['bib']:
#                     if n in ____lines____['bib'][src_]:
#                         src = src_;
#                         break;
#                     continue;
#                 try:
#                     if not src is None and not bibtext[src] is None:
#                         indent = re.sub(r'^(\s*)(\S|).*', r'\1', line);
#                         for bibline in bibtext[src]:
#                             print(indent + bibline, file=____filetex____);
#                             pass;
#                         continue;
#                 except:
#                     pass;
#             if n == nr_lines-1 and line == '':
#                 continue;
#             print(line, file=____filetex____);
#     pass;
#
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
