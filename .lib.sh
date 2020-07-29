#!/bin/bash

export NAME_OF_PROGRAMME="phpytex";
export OUT="/dev/stdout";
export ERR="/dev/stderr";
export VERBOSE="/dev/null";
export CONFIG_LOGGING="logging.yml";
export CONFIG_SETUP="setup.yml";
export BUILD_DIRECTORY="build";
export DIST_DIRECTORY="dist";
export TEST_DIRECTORY="test";
export SOURCE_DIRECTORY="src";

## $1 = full argument string, $2 = key, $3 = default value.
## example:
## value=$(get_kwarg "$@" "name" "N/A");
function get_kwarg() {
    value="$(echo "$1" | grep -E -q "^.*$2=" && echo "$1" | sed -E "s/^.*$2=([^[:space:]]*).*$/\1/g" || echo "")";
    echo $value | grep -E -q "[^[:space:]]" && echo "$value" || echo "$3";
}

## $1 = full argument string, $2 = argument.
## example:
## if [ $(has_arg "$@" "help") ]; then ...
function has_arg() {
    echo "$1" | grep -E -q "^(.*\s|)$2(\s.*|)$" && echo 0 | echo 1;
}

function _fail() {
    MESSAGE="$1";
    echo -e "\033[1;91mERROR\033[0m! $MESSAGE" >> "$ERR";
    exit 1;
}

export PYTHON="env/bin/python3";
[ -f "$PYTHON" ] || _fail "python not found";

export PIP="$PYTHON -m pip";

function _empty() {
    directory="$1";
    if [ -z "$directory" ] || ! [ -d "$directory" ]; then
        return;
    fi
    echo "Cleaning $directory..." >> "$OUT";
    find "$directory" | grep -v ".gitkeep" | grep -v "VERSION" | grep -v "^$directory$" | xargs rm -rf;
}

function _install_to_venv() {
    module="$1";
    # opt="--force-reinstall";
    opt="--upgrade";
    echo "Installing $module" >> "$OUT";
    $PIP install $opt "$module" >> "$VERBOSE" 2>> "$VERBOSE" || _fail "install_using_pip: Failed to install $module";
}

function setup_test() {
    # nothing to do
    return;
}

function setup_build() {
    # nothing to do
    return;
}

function get_version {
    file=$DIST_DIRECTORY/VERSION;
    [ -f "$file" ] || _fail "VERSION file missing in the distribution directory!";
    VERSION="$(cat "$file" | grep -E "^[[:digit:]]+.[[:digit:]]+.[[:digit:]]+$")";
    echo "$VERSION";
}

function run_tests() {
    $PYTHON $TEST_DIRECTORY/main.py $@;
}

function run_programme() {
    $DIST_DIRECTORY/$NAME_OF_PROGRAMME $@;
}
