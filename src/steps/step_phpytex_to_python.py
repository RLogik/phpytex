#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.local.maths import *;
from src.local.typing import *;

from src.core.log import *;
from src.core.utils import createNewFileName;
from src.core.utils import formatTextBlockAsList;
from src.core.utils import readTextFile;
from src.core.utils import unique;
from src.core.utils import writeTextFile;
from src.customtypes.exports import *;
from src.setup import appconfig;
from src.setup.methods import extractPath;
from src.setup.methods import getTemplatePhpytexLines;
from src.parsers.phpytex import parseText;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD: step transpile phpytex to python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def step(lines: List[str]):
    appconfig.setIncludes([]);
    appconfig.setDocumentStructure([]);
    random.seed(appconfig.getSeed()); # <-- only do this once!
    lines[:] = [];
    root = appconfig.getPathRoot();

    params = {
        'no-comm':       (appconfig.getOptionComments() is False),
        'no-comm-auto':  (appconfig.getOptionComments() == 'auto'),
        'show-structure': appconfig.getOptionShowStructure(),
    };

    documents = TranspileDocuments(
        root       = root,
        indentsymb = appconfig.getIndentCharacter()
    );

    addPreamble(
        path      = appconfig.getFileStamp(),
        documents = documents,
        silent    = getQuietMode(),
        params    = params
    );

    addDocument(
        path      = appconfig.getFilePhpytex(),
        documents = documents,
        mute      = False,
        silent    = getQuietMode(),
        params    = params
    );

    createImportFileParameters(
        path      = os.path.join(root, appconfig.getFileParamsPy()),
        overwrite = appconfig.getOptionOverwriteParams(),
        documents = documents
    );

    globalvars = unique(list(appconfig.getExportVars().keys()) + list(documents.variables.keys()));
    fnameLatex, _, _ = extractPath(path=appconfig.getFileLatex(), relative=False, ext='tex');
    fnamePy = createNewFileName(dir=root, nameinit='phpytex_main.py', namescheme='phpytex_main_{}.py');
    createmetacode(
        lines      = lines,
        documents  = documents,
        globalvars = globalvars,
        fname      = fnameLatex,
        fnameOut   = fnamePy
    );

    appconfig.setFileScript(fnamePy);
    # appconfig.setPrecompileLines(_precompile_lines);
    # appconfig.setListOfImports(_list_of_imports);

    logInfo('Transpilation (phpytex -> python) complete.');
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SECONDARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def addPreamble(
    path: str,
    documents: TranspileDocuments,
    params:    Dict[str, bool],
    silent:    bool = False,
):
    # preamble = [];
    struct = appconfig.getDocumentStructure()[:]
    if isinstance(path, str) and not(path == ''):
        appconfig.setDocumentStructure([]);
        addDocument(
            # filecontents = preamble,
            path      = path,
            documents = documents,
            mute      = True,
            params    = params | { 'no-comm': False, 'no-comm-auto': True }
        );
        appconfig.setDocumentStructure(struct[:]);

    # if not silent:
    #     addpytexline(lines=preamble, verbatim=verbatim, expr=[
    #         '%% ********************************************************************************',
    #         '%% DOCUMENT STRUCTURE:',
    #         '%% ~~~~~~~~~~~~~~~~~~~',
    #         '%%',
    #     ] + struct + [
    #         '%%',
    #         '%% DOCUMENT-RANDOM-SEED: '+str(appconfig.getSeed()),
    #         '%% ********************************************************************************',
    #     ], anon=False, mode='meta');

    # lines[:] = preamble + lines;
    # appconfig.setPrecompileLines(verbatim + appconfig.getPrecompileLines());
    return;

def addDocument(
    path:         str,
    documents:    TranspileDocuments,
    params:       Dict[str, bool],
    chain:        List[str]          = [],
    anon:         bool               = False,
    mute:         bool               = False,
    silent:       bool               = False,
):
    if path in chain:
        logError('The document contains a cycle!');
        return;
    try:
        lines = readTextFile(path);
    except:
        logError('Could not find or read document \033[1m{path}\033[0m!'.format(path = path));
        return;
    indentation = IndentationTracker(
        symb       = appconfig.getIndentCharacter(),
        pattern    = appconfig.getIndentCharacterRe(),
        is_legacy  = appconfig.getOptionLegacy(),
    );
    if path in documents.paths:
        return;
    blocks = [];
    for block in parseText(lines, indentation):
        kind = block.kind;
        if re.match(r'^text:comment', kind) and (\
            params['no-comm'] or \
            ( params['no-comm-auto'] and re.match(r'^.*:simple$', kind) ) \
        ):
            continue;
        blocks.append(block);
    documents.addDocument(path=path);
    documents.addBlocks(path=path, blocks=blocks);
    for subpath in documents.getSubPaths(path):
        addDocument(
            path      = subpath,
            documents = documents,
            chain     = chain + [path],
            anon      = anon,
            mute      = mute,
            silent    = silent,
            params    = params
        );
    return;

def createImportFileParameters(
    path:      str,
    overwrite: bool,
    documents: TranspileDocuments
):
    if os.path.exists(path) and not overwrite:
        return;
    lines = formatTextBlockAsList(
        '''
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-
        '''
    );
    lines.append('');
    names = appconfig.getExportVars().keys();
    for name, (value, codedvalue) in appconfig.getExportVars().items():
        lines.append('{name} = {codedvalue};'.format(name=name, codedvalue=codedvalue));
    for name in documents.variables.keys():
        if name in names:
            continue;
        lines.append('{name} = None;'.format(name=name));
    lines.append('');
    writeTextFile(path=path, lines=lines, force_create_path=True);
    return;

def createmetacode(
    lines:      List[str],
    documents:  TranspileDocuments,
    fname:      str,
    fnameOut:   str,
    globalvars: List[str]
):
    imports = []; ## TODO: extract immports from special code-blocks
    lines[:] = documents.generateCode(globalvars=globalvars);
    fname_rel, _, _ = extractPath(path=fname, relative=True, ext='');
    _phpytex_lines = getTemplatePhpytexLines()
    lines_pre = formatTextBlockAsList(
        _phpytex_lines.format(
            import_params = 'from {name} import *;\n'.format(name = appconfig.getImportParamsPy()),
            indentchar    = appconfig.getIndentCharacterRe(),
            fname         = fname,
            fname_rel     = fname_rel,
            maxlength     = appconfig.getMaxLengthOuput(),
            insertbib     = appconfig.getOptionInsertBib(),
            rootdir       = appconfig.getPathRoot(),
            seed          = appconfig.getSeed(),
            imports       = '\n    '.join(imports if len(imports) > 0 else [ '# no imports' ]),
        )
    );
    appconfig.setLenPrecode(len(lines_pre));
    lines[:] = lines_pre + lines;
    ## create temp file and write to this:
    writeTextFile(fnameOut, lines);
    return;
