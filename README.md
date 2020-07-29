# (Ph(P)y)TeX and (Ph(P)y)create #

This project (will!) contain versioned releases of the programmes (compiled as single binaries) as well as a more clearer and thus easier to understand and debug project structure. For our project compilation, we rely on `PyInstaller`, which in turn limits us to using Python 3.0–3.6.

The old project files (unversioned) will be kept (for now) in the repository [RLogik/phpytex-old](https://github.com/RLogik/phpytex-old).

## tl; dr ##

**What is phpytex?** Simply put it's an augmented language and a transpiler for latex. Here are the key features:

- You can augment your tex/latex files with python code.
- Some commands are inspired by PHP, hence the combined name.
- There are generally on the market place 2 kinds of code + latex fusions:
  - ones that are written entirely in the programming language;
  - ones (like markdown, Rmd, pandocs) which allow a hybrid.

  Phpytex is written less like the former, is intended to be more like the latter,
  except with the ability to work with a tree structure of files.
- **Transpiling** means in this context that the augmented code is first converted to pure latex (and then compiled with `pdflatex`).
- The result of transpilation is a **single file**, including all bib entries which is great for submissions to journals---it suffices to submit just one tex file (+ images).

So you can work faster, with project structures, an still create a single file output. The second component, **phpycreate**, allows one to write a single **yaml** file and generate a project structure, without having to manually create a lot of (sub)folders and files. It is also designed to allow one to knit together projects.

## Contents ##

- [History](#history)
- [Installation](#setup)
- [Usage (short)](#usage-short)
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

In 2019 I continue to improve phpytex, but simply overwrote my changes. I artificially added version numbers, but was painfully aware that this not be best practice. A proper project structure was needed and a proper archive of release versions, as well as testing. That is the aim of this revived project. As of 28.07.2020, the phpytex project under this new vision will be actively developed.

## <a name="usage-short">USAGE (short)</a> ##

(_Under construction!_)

## <a name="usage-long">USAGE (full)</a> ##

(_Under construction!_)

## <a name="project">DETAILS OF THIS PROJECT</a> ##

(_Under construction!_)
