#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
import os
import re

from ...._core.logging import *
from ...._core.utils.basic import *
from ...._core.utils.misc import *
from ...._core.utils.system import *
from ....models.enums import *
from ....models.transpilation import *
from ....models.user import *
from ....parsers import parser_phpytex
from ....queries import user
from ....setup import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "step_transpile",
]

# ----------------------------------------------------------------
# METHOD: step transpile phpytex to python
# ----------------------------------------------------------------


@echo_function(tag="STEP TRANSPILE ([phpytex -> py] -> ...)", level="INFO", close=True)
def step_transpile(cfg_user: UserConfig):
    options = cfg_user.compile.options
    indentsymb = user.setting_indent_character()

    # only do this once!
    reseed(seed=options.seed, legacy=True)

    # Initialise structures for recording transpilation units:
    preambles = []
    imports = TranspileBlocks()
    documents = TranspileDocuments(
        root=os.getcwd(),
        indentsymb=indentsymb,
        schemes=dict(file=FUNCTION_NAME_FILE, main=FUNCTION_NAME_MAIN, pre=FUNCTION_NAME_PRE),
    )

    # Transpile preamble:
    log_console(".")
    if cfg_user.stamp is not None:
        name = "stamp"
        preambles.append(name)
        transpileDocument(
            options=options,
            path=cfg_user.stamp.file,
            documents=documents,
            imports=TranspileBlocks(),
            name=name,
            is_preamble=True,
            silent=True,
            params={"comm": True, "comm-auto": False, "show-tree": False},
            lex=[False],
        )

    # Transpile document file:
    transpileDocument(
        options=options,
        path=options.root,
        documents=documents,
        imports=imports,
        name="",
        is_preamble=False,
        silent=config.quiet_mode(),
        params={
            "comm": options.comments == EnumCommentsOptions.ON,
            "comm-auto": options.comments == EnumCommentsOptions.AUTO,
            "show-tree": options.show_structure,
        },
        lex=[True],
    )

    # Add document structure:
    name = "tree"
    if options.show_structure:
        preambles.append(name)

    blocks = TranspileBlocks([documents.documentTree(seed=options.seed)])
    documents.addPreamble(name=name, blocks=blocks)

    # Handle global parameters:
    if cfg_user.parameters is not None:
        cfg_user.parameters.overwrite
        modulename = cfg_user.parameters.file

        # Create file:
        path = re.sub(r"([^\.]+)\.", r"\1/", modulename) + ".py"
        createImportFileParameters(
            path=path,
            overwrite=cfg_user.parameters.overwrite,
            documents=documents,
        )

        # Add import block for global parameters:
        imports.append(
            TranspileBlock(
                kind="code",
                content=f"from {modulename} import *;",
                level=0,
                indentsymb=indentsymb,
            )
        )

    # Generate result of transpilation (phpytex -> python):
    createmetacode(
        options=options,
        documents=documents,
        imports=imports,
        preambles=preambles,
        globalvars=list(user.EXPORT_VARS.keys()) + list(documents.variables.keys()),
        seed=options.seed,
    )
    return


# ----------------------------------------------------------------
# SECONDARY METHODS
# ----------------------------------------------------------------


def transpileDocument(
    options: UserConfigPartCompileOptions,
    path: str,
    documents: TranspileDocuments,
    imports: TranspileBlocks,
    chain: list[str] = [],
    name: str = "",
    is_preamble: bool = False,
    silent: bool = False,
    params: dict[str, bool] = dict(),
    lex: list[bool] = [],
):
    if path in chain:
        logging.error("The document contains a cycle!")
        return
    try:
        with open(path, "r") as fp:
            lines = "".join(fp.readlines())

    except Exception as _:
        logging.error("Could not find or read document \033[1m{path}\033[0m!".format(path=path))
        return

    indentsymb = user.setting_indent_character()
    indentation = IndentationTracker(
        symb=indentsymb,
        pattern=user.setting_indent_character_re(),
    )

    if is_preamble:
        blocks = TranspileBlocks()
        for block in parser_phpytex.parse(lines, indentation, offset=options.offset):
            if not (block.kind == "text:comment"):
                continue
            blocks.append(block)

        blocks.append(TranspileBlock(kind="text:empty"))
        documents.addPreamble(name=name, blocks=blocks)
        branch = display_tree_branch(
            path=path,
            anon=False,
            lex=lex,
        )
        log_console(branch)

    else:
        if path in documents.paths:
            return

        documents.addDocument(path=path)
        ## NOTE: need to do this first, in order to update anon-state
        anon = documents.isAnon(path=path)
        hide = documents.isHidden(path=path)
        blocks = TranspileBlocks()
        branch = display_tree_branch(
            path=path,
            anon=anon,
            lex=lex,
        )
        log_console(branch)

        if params["show-tree"]:
            blocks.append(documents.documentStamp(depth=0, start=True, anon=anon, hide=hide))

        for block in parser_phpytex.parse(lines, indentation, offset=options.offset):
            if block.kind == "code:import":
                imports.append(block)
                continue

            if block.kind == "text:comment":
                if params["comm-auto"] == True:
                    if not block.parameters.keep:
                        continue

                elif params["comm"] == False:
                    continue

            blocks.append(block)

        if params["show-tree"]:
            blocks.append(documents.documentStamp(depth=0, start=False, anon=anon, hide=hide))

        documents.addBlocks(path=path, blocks=blocks)
        subpaths = documents.getSubPaths(path)
        n = len(subpaths)
        for k, subpath in enumerate(subpaths):
            is_final = k == n - 1
            transpileDocument(
                options=options,
                path=subpath,
                documents=documents,
                imports=imports,
                chain=[*chain, path],
                silent=silent,
                params=params,
                lex=[*lex, is_final],
            )
    return


def createImportFileParameters(
    path: str,
    overwrite: bool,
    documents: TranspileDocuments,
):
    if os.path.exists(path) and not overwrite:
        return

    lines = []
    lines += dedent_split(
        """
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-

        from fractions import Fraction;
        """
    )
    lines.append("")

    data = {key: None for key, value in documents.variables.items()} | {
        key: coded_value for key, (_, coded_value) in user.EXPORT_VARS.items()
    }
    lines += [f"{key} = {coded_value}" for key, coded_value in data.items()]
    lines.append("")

    write_text_file(path=path, lines=lines)
    return


def createmetacode(
    options: UserConfigPartCompileOptions,
    documents: TranspileDocuments,
    imports: TranspileBlocks,
    preambles: list[str],
    globalvars: list[str],
    seed: int | None,
):
    _lines_pre = get_template_phpytex_lines_pre()
    _lines_post = get_template_phpytex_lines_post()
    align = options.align
    lines = []
    lines += dedent_split(
        _lines_pre.format(
            imports="\n".join(imports.generateCode(align=align)),
            root=os.getcwd(),
            output=options.output,
            name=os.path.splitext(options.output)[0],
            insert_bib=options.insert_bib,
            backend_bib=options.backend_bib,
            compile_latex=options.compile_latex,
            length_max=options.max_length,
            seed=seed,
            indentsymb=user.setting_indent_character(),
            censorsymb=options.censor_symbol,
            mainfct=FUNCTION_NAME_MAIN,
        )
    )
    lines.append("")
    lines += documents.generateCode(
        offset=0,
        preambles=preambles,
        globalvars=unique(globalvars),
        align=align,
    )
    lines.append("")
    lines += dedent_split(_lines_post.format())
    write_text_file(options.transpiled, lines)
    return


# ----------------------------------------------------------------
# METHOD: step transpile phpytex to python
# ----------------------------------------------------------------


def display_tree_branch(
    path: str,
    anon: bool = False,
    lex: list[bool] = [],
) -> str:
    if len(lex) == 0:
        is_final = True
        sep = ""

    else:
        is_final = lex[-1]
        sep = "└──  " if is_final else "├──  "

    indent = "  "
    path = "*****" if anon else path
    prefix = "".join([
        (" " if is_last else "│") + indent
        for is_last in lex[:-1]
    ])  # fmt: skip

    return f"{prefix}{sep}{path}"
