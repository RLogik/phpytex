# (PH(p)y)TeX #

Phpytex transpiles hybrid code (ordinary LaTeX files augmented by blocks of python code)
to a python script, which in turn generates a single LaTeX file
(which in turn may be optionally compiled to pdf), _i.e._

```
augmented code ⟶ python script ⟶ single .tex [⟶ pdf]
```

### Why Phpytex? There are lots of transpilers out there! ###

There are many _(insert language here)_-to-LaTeX transpilers available.
And many of these do all sorts of fancy things like incorporate lots of
extra special syntax to embed plots, _etc._
By contrast our transpiler is intentionally designed to be 'boring' (=sufficently general)!
It has no built-in _'We can produce these cool graphics with this one command!'_<sup>[[1]](#footnote_1)</a></sup> selling point.

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

### But what exactly does it do? Show me examples! ###

See the [examples](./examples) subfolder for some examples.
Each case contains a set of initial files and a counterpart folder with the outputs.

## Getting started ##
### System requirements ###

- Bash (windows users may install [git/bash for windows](https://gitforwindows.org))
- Python 3 (currently developed under python 3.9.5)

### Installation ###

Follow the instructions in [install/README.md](./install/README.md).
This will enable you to call `phpytex` within any project containing a `.phpytex.yml` config file.

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

<br/>
<br/>
<br/>
<br/>

<tt>----------------</tt>
<br/>
<div style='font-size:10pt'>
<a name='footnote_1'>[1]</a> But incidentally, with phpytex one can do this and just about any such task.
The user simply has to program their own methods, say a python function <tt>makegraphics(...)</tt>
in a code block or an importable script, and ensure this method takes desired inputs and
<i>either</i> generates an image and returns suitable LaTeX command to include this,
<i>or</i> returns a series of LaTeX commands (_e.g._ <tt>tikz</tt> commands)
to produce the image natively in LaTeX.

One can clearly make a standard suite of such functions.
But creating such things should not be in the scope of a good, sufficiently general, transpiler,
but rather of package development.
</div>
