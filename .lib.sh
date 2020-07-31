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

## $1 = full argument string
## $2 = key (including connecter: either = or space)
## $3 = new-key (ditto)
## $4 = true/false whether to force quotation marks on values.
## example:
## value=$(get_all_kwargs "$@" "degree " "major=" true);
function get_all_kwargs() {
    arguments="$1";
    key="$2";
    new_key="$3";
    force_quotes="$4";

    pattern="(^.*[[:space:]]|^)$key([^[:space:]]*).*$";
    new_arguments="";
    while ! [[ "$arguments" == "" ]]; do
        if ! ( echo $arguments | grep -E -q "$pattern" ); then
            arguments="";
            break;
        fi
        value="$(echo "$arguments" | sed -E "s/$pattern/\2/g" || echo "")";
        arguments="$(echo "$arguments" | sed -E "s/$pattern/\1/g" || echo "")";
        if [[ "$force_quotes" == "true" ]]; then
            new_arguments="$new_key\"$value\" $new_arguments"
        else
            new_arguments="$new_key$value $new_arguments"
        fi
    done
    echo $new_arguments;
}

## $1 = full argument string, $2 = argument.
## example:
## if [ $(has_arg "$@" "help") ]; then ...
function has_arg() {
    echo "$1" | grep -E -q "^(.*\s|)$2(\s.*|)$" && echo 0 | echo 1;
}

function check_answer() {
    echo "$1" | grep -q -E -i "^(y|yes|j|ja|1)$";
}

function _fail() {
    MESSAGE="$1";
    echo -e "\033[1;91mERROR\033[0m! $MESSAGE" >> "$ERR";
    exit 1;
}

export PYTHON="env/bin/python3";
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

function post_build_create_release_version() {
    VERSION="$(get_version)";
    file="$NAME_OF_PROGRAMME";
    file_zip="$file.zip";
    file_zip_version="$file-$VERSION.zip";

    # check if binary exists:
    [ -f "$DIST_DIRECTORY/$file" ] || _fail "Programme file missing in the distribution directory!";
    # check if version already exists:
    if [[ -f "$DIST_DIRECTORY/$file_zip_version" ]]; then
        echo -n -e "\033[1;91mWarning\033[0m: Version \033[1;92m$VERSION\033[0m already exists! Are you sure you wish to overwite this? (y/n) ";
        read answer;
        if ! ( check_answer "$answer" ); then
            echo -e "The release '\033[1;94m$file_zip_version\033[0m' will not be overwritten.";
            return;
        else
            echo -e "The release '\033[1;94m$file_zip_version\033[0m' will be \033[1;91moverwritten\033[0m.";
        fi
        echo -e "";
    fi

    # create zip
    echo -e "Creating zip for version \033[1;92m$VERSION\033[0m..." >> "$OUT";
    echo -e "";
    zip -r "$DIST_DIRECTORY/$file_zip_version"  \
            "./README.md" \
            "$BUILD_DIRECTORY/lib" \
            "$DIST_DIRECTORY/$file" \
            "$DIST_DIRECTORY/VERSION" \
        >> "$OUT" 2>> "$ERR" \
        && cp "$DIST_DIRECTORY/$file_zip_version" "$DIST_DIRECTORY/$file_zip";
    echo -e "";
    echo -e "...done" >> "$OUT";
    echo -e "";
}

function get_version {
    file=$DIST_DIRECTORY/VERSION;
    [ -f "$file" ] || _fail "VERSION file missing in the distribution directory!";
    cat "$file" | grep -E "^[[:digit:]]+.[[:digit:]]+.[[:digit:]]+$";
}

function run_tests() {
    [ -f "$PYTHON" ] || _fail "Python not found!";
    $PYTHON $TEST_DIRECTORY/main.py $@;
}

function run_programme() {
    programme="$DIST_DIRECTORY/$NAME_OF_PROGRAMME";
    [ -f "$programme" ] || _fail "Binary of $NAME_OF_PROGRAMME could not be found!";
    $programme $@;
}
