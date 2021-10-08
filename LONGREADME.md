# (PH(p)y)TeX - Longer README #

This project contains versioned releases of the programme, which combines both original programmes.

The old project files (unversioned) will be kept (for now) in the repository [RLogik/phpytex-old](https://github.com/RLogik/phpytex-old).

This project currently uses `python==3.9.5`.

**What is phpytex?** Simply put it's an augmented language and a transpiler for LaTeX.
<br>
Key features

- You can augment your tex/LaTeX files with **python** code.
- Some commands are inspired by PHP, hence the name.
- There are generally on the market place 2 kinds of code + LaTeX fusions:
  - ones that are written entirely in the programming language;
  - ones like markdown, Rmd, pandocs, _etc._ which allow a hybrid, but require everything to be written in one file.

  Phpytex is written less like the former, is intended to be more like the latter,
  except with the ability to work with a tree structure of files.
- **Transpiling** means in this context that the augmented code is first converted to pure python code,
    which then produces pure latex (which may then be compiled with `pdflatex`).
- The result of transpilation is a **single file**,
    including all bib entries which is great for submissions to journals—it suffices to submit just one tex file (+ images).

This allows users to work faster, cleaner (with project structures), and still create a single file output.

## Contents ##

- [History](#history)
- [Installation](#setup)
- [Usage - quick start](#usage-short)
- [Usage (full)](#usage-long)
  - [Project setup](#setup)
  - [Python Commands](#py-cmd)
    - Python
    - The PHP-inspired commands — ‘Quick-Python‘
  - [Python Variables in LaTeX](#py-var)
  - [Examples](#bsp)
  - [Special commands/-variables in Python](#bes-var)
  - [The phpytex Compiler](#compiler)
    - [Compilation process](#compile-zyklus)
    - [\input und \bibliography](#input-bib)
    - [Indentation + Examples](#indentation)
    - [Parsing of py/PHP-expressions + Examples](#parsing)
- [Details of this project](#project)
  - [Setup](#project-setup)
  - [Usage](#project-usage)
  - [Contribution](#project-contribution)
  - [Releases](#project-releases)

## <a name="history">HISTORY</a> ##

The key reason I wrote phpytex (some time around early/mid 2018) was quite simply out of necessity. I needed to write a single tex file, but I wanted to retain working with project structures. Most people with sufficient coding background do this in general too, as working with a hopelessly long file is impracticable, difficult to maintain, and frustrating to use.

The second primary reason was that want wanted to access the full robustness of a half decent programming language. TeX/LaTeX is _not_ a programming language—its strength is producing (very) nice pdfs and it is based on a (frustrating) macro-expansion logic. I always wanted to enhance latex with some programming language, and the former necessity provided the occasion to do so.

In 2019, I continued to improve phpytex, but simply overwrote my changes. I artificially added version numbers, but was painfully aware that this not be best practice. A proper project structure was needed and a proper archive of release versions, as well as testing. That is the aim of this revived project. As of 28.07.2020, the phpytex project under this new vision will be actively developed.

## <a name="setup">INSTALLATION</a> ##

Follow the instructions in [install/README.md](./install/README.md).
This will enable you to call `phpytex` within any project containing a `.phpytex.yml` config file.
## <a name="usage-short">USAGE - QUICK START</a> ##

- `phpytex` or `phpytex help` displays a message with the commands.
- `phpytex version` displays in plain text the version number.
- `phpytex run [file=<name of config file>]` runs the programme within a project using the named config file.
  </br>
  If the `file` flag is left empty, the programme searches for the first yaml-file matching the pattern `*.(phpytex|phpycreate).(yml|yaml)` and uses this as the config file.

### <a name="usage-short_config">Set up of config file</a> ###

To use phpytex, a `.phpytex.yml` file is required in the (root of) the project folder.
This should contain 4 parts with the following structure:

```yaml
ignore:      false # (optional) whether or not to skip this project.
################################################################################
# COMPILE OPTIONS - control how `phpytex run` should processes your project
################################################################################
compile:
  # legacy:     false    # true => chooses options customised for legacy documents.
  #                      # (default=false)
  root:       root.tex # path to starting document relative to root folder.
  output:     main.tex # desired name of transpiled output file.
  debug:      false    # true = stop transpilation before generation of latex file
  compile:    true     # true = full compilation: phpytex -> python -> latex -> pdf
                       #        (only works if debug=false is set).
  insert-bib: true     # true = after compilation, <<< bibliograph >>> command
                       #        replaced by bbl-file content.
  comments:   auto     # Handling of comments:
                       #   true = allow all comment lines
                       #   false = remove all comment lines
                       #   auto = remove only those comment lines
                       #          starting with a single %
                       #          E.g. '%% test' will be retained.
                       #   (default=auto)
  show-tree:  true     # true = output file (main.tex) will contain information
                       #        about document structure displayed as comments.
  max-length: 10000    # Safeguard against infinite documents!
  tabs:       false    # true -> python blocks use \t; false -> use n spaces.
  spaces:     4        #
  # offset:     '    '  # minimal offset inside code blocks, defaults to empty string.
  seed:       4627833  # any (not too large) integer to see the RNG.
################################################################################
# STAMP OPTIONS - Defines a comment block at the start of main.tex output
# (optional)      Useful for recording meta information.
################################################################################
stamp:
  file: stamp.tex      # desired name of file.
  overwrite: true      # whether or not to overwrite existing file.
  options:             # <- one can set arbitrary key-value arguments.
    author:    Max Mustermann
    created:   27.08.2021
    edited:    28.08.2021
    title:     &title The stages of artificial intelligence beyond human intelligence
    institute: Faculty of mathematics
################################################################################
# DOCUMENT PARAMETERS - Defines global params to be used throughout the project.
# (optional)            Useful for managing complex document structures.
################################################################################
parameters:
  file: src.parameters  # desired location of file (as python import).
  overwrite: true       # whether or not to overwrite existing file.
  options:              # <- one can set arbitrary key-value arguments.
    FONT_SIZE: 12pt         # usage in document: <<< FONT_SIZE >>>
    TITLE:     *title       # usage in document: <<< TITLE >>>
    KEYWORDS:
      - ai
      - computer science    # usage in document: <<< KEYWORDS[1] >>>
      - research
################################################################################
# DOCUMENT TREE - Allows creation of arbitrary folders/files in project.
# (optional)      NOTE: existing files will not be overwritten.
################################################################################
files:
  - root.tex
  - title.tex
  - contents.tex
folders:
  body:
    files:
     - introduction.tex
     - definitions.tex
     - parts.tex
    folders:
  ## the files / folders dictionary may be arbitrarily nested
```

Within documents use `<<< input 'path-to-file' >>>` or `<<< input_anon 'path-to-file' >>>`
to input a file or to do this anonymously (will be excluded from final output).
</br>
Similarly `<<< bibliography 'path-to-bib-file' >>>` and `<<< bibliography_anon 'path-to-bib-file' >>>`
may be used to indicated the inclusion of a bib-file.
</br>
Note that the path is always taken to be relative to the folder of the current document.
</br>
For example within `body/parts.tex` the following commands are equivalent:

```coffee
<<< input 'part-one/definitions.tex' >>>
<<< input __DIR__ + '/part-one/definitions.tex' >>>
<<< input __ROOT__ + '/body/part-one/basic-concepts.tex' >>>
```

The dynamic `__ROOT__` variable is useful if one wishes to input files from adjacent subfolders.

## <a name="usage-long">USAGE - FULL</a> ##

(_Under construction!_)

## <a name="project">DETAILS OF THIS PROJECT</a> ##

(_Under construction!_)
