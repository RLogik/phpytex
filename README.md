# (PH(p)y)TeX #

Phpytex transpiles hybrid code (ordinary LaTeX files augmented by blocks of python code)
to a python script, which in turn generates a single LaTeX file
(which in turn may be optionally compiled to pdf), _i.e._

```text
augmented code ⟶ python script ⟶ single .tex [⟶ pdf]
```

## What exactly does it do? Show me examples! ##

Phpytex allows you interweave inline python code, python code blocks,
and text blocks across multiple files, incorporating global variables and imports.
It allows you to manage complex document structures and generate single file outputs.
This can be demonstrated in the cases in the [examples](./examples) subfolder.
Each case contains a set of initial files and a counterpart folder with the outputs.

## Getting started ##

### System requirements ###

- Bash (windows users may install [git/bash for windows](https://gitforwindows.org))
- python `^3.11`

### Installation ###

The following steps are flexible:

1. Create/choose a path, e.g. `$HOME/.phpytex`:

    ```bash
    mkdir -p "$HOME/.phpytex"
    mkdir -p "$HOME/.phpytex/bin"
    ```

2. Ensure that the latter path (for the binaries) is part of your `$PATH` variable:

    ```bash
    # only needed once, if not already created
    touch $HOME/.bash_profile
    # permanently adds the path - the file can also be manually editted
    echo "export \${PATH}=\"\${PATH}:\${HOME}/.phpytex/bin\"" >> ${HOME}/.bash_profile
    ```

3. Clone or download a repository zip artefact (see the [Releases](releases) page).

4. Rename the folder to `X.Y.Z` and store it under `$HOME/.phpytex/X.Y.Z`.

5. Navigate to `$HOME/.phpytex/X.Y.Z`.

    1. Run `just setup` and update the `.env` file.

    2. Run `just build-deployment`

6. Navigate to `$HOME/.phpytex/bin`.
   Create a bash script called `phpytex`

    ```sh
    #!/usr/bin/env bash

    VERSION="X.Y.Z" # <- the current version

    dist="$( dirname $( dirname "${0}" ) )/${VERSION}"
    jf="${dist}/justfile"

    if [[ ${#@} == 1 ]] && [[ "$1" == "run" ]]; then
        just --justfile "${jf}" run-cli  "run" "TRANSPILE" --path "${PWD}"
    else
        just --justfile "${jf}" run-cli  "$@"
    fi
    ```

    and store this as `$HOME/.phpytex/bin/phpytex`.

7. Assign execution permissions to the file via

    ```bash
    chmod +x "$HOME/.phpytex/bin/phpytex"
    ```

Test it out:

  ```bash
  phpytex --version
  ```

NOTE: you may need to restart the bash session in advance
to ensure the binaries are included in `$PATH`.

### Usage - quick start ###

- `phpytex` or `phpytex help` displays a message with the commands.
- `phpytex version` displays in plain text the version number.
- `phpytex run [file=<name of config file>]` runs the programme within a project using the named config file.
  </br>
  If the `file` flag is left empty, the programme searches for the first yaml-file matching the pattern `*.(phpytex|phpycreate).(yml|yaml)` and uses this as the config file.

### Set up of config file ###

To use phpytex, a `.phpytex.yml` file is required in the (root of) the project folder.
This should contain 4 parts with the following structure:

```yaml
########################################
# COMPILE OPTIONS
########################################
compile:
  options:
    root:   root.tex
    output: main.tex
    ...
########################################
# STAMP OPTIONS (optional)
########################################
stamp:
  file:      stamp.tex
  overwrite: true
  options:
    ...
########################################
# DOCUMENT PARAMETERS (optional)
########################################
parameters:
  file: src.parameters
  overwrite: true
  options:
  ...
########################################
# DOCUMENT TREE (optional)
########################################
files:
  ...
folders:
  ...
```

See [LONGREADME.md](./LONGREADME.md#usage-short_config) for more details
and see the [examples](./examples) subfolder for concrete examples.

## But why Phpytex? There are lots of transpilers out there! ##

There are many _(insert language here)_-to-LaTeX transpilers available.
And many of these do all sorts of fancy things like incorporate lots of
extra special syntax to embed plots, _etc._
By contrast our transpiler is intentionally designed to be 'boring' (=sufficently general)!
It has no built-in _'We can produce these cool graphics with this one command!'_<sup>[1](#footnote_1)</a></sup> selling point.

And neither—in our opinion—does it need to.

By our philosophy, the only things a transpiler should do are:

- assume the user can already use {python,LaTeX};
- _not_ burden the user with a bunch of extra syntax beyond an absolute minimum
  (_e.g._ markdown languages achieve this wonderfully);
- reliably incorporate the full generality of features of an ordinary (python) coding project; and
- leave the _bells-and-whistles_
  (generation of graphics, usage of complex mathematical objects, data-frames, _etc._)
  completely over to the user's imagination and mastery of both languages.

That is, transpilation allows the user to marry the two languages with little effort
but in as generic a manner as possible,
leaving the specific applications over to the user.

Furthermore Phpytex was originally conceived for the personal reason to

- allow the user to easily manage complex folder structures and generate a single-file-output.

And this shall remain a cornerstone feature of Phpytex.

<br/>
<br/>
<br/>
<br/>

----

<div style='font-size:8pt'>
<a name='footnote_1'><b>[1]</b></a> But incidentally, with Phpytex one can do this and just about any such task.
The user simply has to program their own methods, say a python function <tt>makegraphics(...)</tt>
in a code block or an importable script, and ensure this method takes desired inputs and
<i>either</i> generates an image and returns suitable LaTeX command to include this,
<i>or</i> returns a series of LaTeX commands (<i>e.g.</i> <tt>tikz</tt> commands)
to produce the image natively in LaTeX.

One can clearly make a standard suite of such functions.
But creating such things should not be in the scope of a good, sufficiently general, transpiler,
but rather of package development.
</div>
