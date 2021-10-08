# (PH(p)y)TeX #

The Phpytex programme enables

- python-augmented LaTeX;
- generation of a single tex-file from a project structure;
- managing of complex document structures via single (yaml) config files containing
  - parameter definitions;
  - (creation of) folder and file structures.

Phpytex transpiles hybrid code (ordinary LaTeX files augmented by blocks of python code)
to a python script, which in turn generates a single LaTeX file
(which in turn may be optionally compiled to pdf).

## What does it do? Show me examples! ##

See the [examples](./examples) subfolder.

## System requirements ##

- Bash (windows users may install [git/bash for windows](https://gitforwindows.org))
- Python 3 (currently developed under python 3.9.5)

## Installation ##

Follow the instructions in [install/README.md](./install/README.md).
This will enable you to call `phpytex` within any project containing a `.phpytex.yml` config file.

## Usage - quick start ##

- `phpytex` or `phpytex help` displays a message with the commands.
- `phpytex version` displays in plain text the version number.
- `phpytex run [file=<name of config file>]` runs the programme within a project using the named config file.
  </br>
  If the `file` flag is left empty, the programme searches for the first yaml-file matching the pattern `*.(phpytex|phpycreate).(yml|yaml)` and uses this as the config file.

### Set up of config file ###

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
# STAMP OPTIONS - (optional) defines a comment block at the start of main.tex output
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
# DOCUMENT PARAMETERS - (optional) defines global parameters.
#                       Useful for managing complex document structures.
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
# DOCUMENT TREE - (optional) allows users to create folders/files
#                 NOTE: existing files will not be overwritten.
################################################################################
files:
  - root.tex
folders:
  src:
    files:
      - methods.py
      - packages.tex
      - layout.tex
      - macros.tex
  front:
    files:
      - contents.tex
      - title.tex
      - abstract.tex
  body:
    files:
     - foreword.tex
     - parts.tex
    folders:
      part-one:
        files:
          - definitions.tex
          - basic-concepts.tex
      part-two:
        files:
          - results.tex
   back:
     files:
       - literature.bib
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
