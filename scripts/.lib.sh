#!/usr/bin/env bash

##############################################################################
#    DESCRIPTION: Library of methods specifically for the project.
#    Include using source .whales/.lib.sh
##############################################################################

source scripts/.lib.globals.sh;
source scripts/.lib.utils.sh;

##############################################################################
# GLOBAL VARIABLES
##############################################################################

env_from ".env" import REQUIREMENTS_GO     as PATH_REQ_GO;
env_from ".env" import REQUIREMENTS_PY     as PATH_REQ_PY;
env_from ".env" import NAME_OF_APP;

export CONFIGENV="data/.env";
export PYTHON_APP_PREFIX=\
'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-'''
export USE_VENV=false;

##############################################################################
# AUXILIARY METHODS: Zip
##############################################################################

function create_zip_archive() {
    zip -r $@;
}

##############################################################################
# AUXILIARY METHODS: Go
##############################################################################

function call_go() {
    go $@;
}

function install_requirements_go() {
    local path="$1";
    local cwd="$PWD";
    pushd src-go >> $VERBOSE;
        # go mod tidy; # <- use to detect unused packages in project
        remove_file "go.sum";
        _log_info "Add go requirements";
        call_go get "$( cat "$cwd/$path" )";
    popd >> $VERBOSE
}

function compile_go() {
    _log_info "Compile \033[1mmain.go\033[0m with \033[1mgolang\033[0m";
    local cwd="$PWD";
    remove_file "dist/$NAME_OF_APP";
    pushd src-go >> $VERBOSE;
        call_go build -o $cwd/dist/$NAME_OF_APP "main.go";
    popd >> $VERBOSE;
    ! [ -f "dist/$NAME_OF_APP" ] && exit 1;
}

##############################################################################
# AUXILIARY METHODS: Python
##############################################################################

function use_python_venv_true() { USE_VENV=true; }
function use_python_venv_false() { USE_VENV=false; }

function create_python_venv() {
    ! ( $USE_VENV ) && return;
    _log_info "Create VENV";
    ! [ -d build ] && mkdir build;
    pushd build >> $VERBOSE;
        call_python -m venv env;
    popd >> $VERBOSE;
}

function activate_python_venv() {
    ! ( $USE_VENV ) && return;
    if ( is_linux ); then
        source build/env/bin/activate;
    else
        source build/env/Scripts/activate;
    fi
}

function deactivate_python_venv() {
    ! ( $USE_VENV ) && return;
    if ( is_linux ); then
        source build/env/bin/deactivate;
    else
        source build/env/Scripts/deactivate;
    fi
}

function call_python() {
    if ( is_linux ); then
        python3 $@;
    else
        py -3 $@;
    fi
}

function call_v_python() { activate_python_venv && call_python $@; }

function call_utest() { call_python -m unittest discover $@; }

function call_v_utest() { activate_python_venv && call_utest $@; }

function call_pipinstall() {
    # Do not use --user flag with venv
    DISPLAY= && call_python -m pip install $@;
}

function install_requirements_python() {
    local path="$1";
    local has_problems=false;
    local problem_packages=();

    dos_to_unix "$path";
    local line;
    while read line; do
        line="$( _trim_trailing_comments "$line" )";
        [ "$line" == "" ] && continue;
        _log_info "Run \033[92;1mPIP\033[0m to install \033[93;1m$line\033[0m...";
        ( call_pipinstall "$line" >> $VERBOSE ) && continue;
        has_problems=true;
        problem_packages+=( "$line" );
    done <<< "$( cat "$path" )";

    ( $has_problems ) && _log_fail "Something went wrong whilst using \033[92;1mPIP\033[0m to install: {\033[93;1m${problem_packages[*]}\033[0m}.";
}

function install_requirements_v_python() { activate_python_venv && install_requirements_python $@; }

##############################################################################
# AUXILIARY METHODS: APT-GET
##############################################################################

function run_install_apt() {
    apt-get install -y $@;
}

function install_requirements_aptget() {
    local path="$1";
    local has_problems=false;
    local problem_packages=();

    local line;
    while read line; do
        line="$( _trim_trailing_comments "$line" )";
        [ "$line" == "" ] && continue;
        _log_info "Run \033[92;1mAPT-GET\033[0m install \033[93;1m$line\033[0m...";
        ( run_install_apt "$line" >> $VERBOSE ) && continue;
        has_problems=true;
        problem_packages+=( "$line" );
    done <<< "$( cat "$path" )";

    ( $has_problems ) && _log_fail "Something went wrong whilst using \033[92;1mAPT-GET\033[0m to install: {\033[93;1m${problem_packages[*]}\033[0m}.";
}

##############################################################################
# AUXILIARY METHODS: CLEANING
##############################################################################

function garbage_collection_build() {
    clean_folder_contents "build";
}

function garbage_collection_python() {
    clean_all_folders_of_pattern ".DS_Store";
    local path;
    for path in "src" "test"; do
        pushd "$path" >> $VERBOSE;
            # clean_all_files_of_pattern "*\.pyo";
            clean_all_folders_of_pattern "__pycache__";
        popd >> $VERBOSE;
    done
}

function garbage_collection_dist() {
    remove_file "dist/$NAME_OF_APP";
}

##############################################################################
# MAIN METHODS: PROCESSES
##############################################################################

function run_setup() {
    _log_info "RUN SETUP";
    create_python_venv;
    _log_info "Check and install missing requirements";
    install_requirements_v_python "$PATH_REQ_PY";
}

function run_setup_go() {
    install_requirements_go "$PATH_REQ_GO";
}

function run_create_artefact() {
    local current_dir="$PWD";
    ## create temp artefacts:
    local _temp="$( create_temporary_dir "dist" )";
    copy_dir dir="src" from="." to="$_temp";
    copy_file file="VERSION" from="dist" to="${_temp}/src/setup";
    mv "${_temp}/src/__main__.py" "$_temp";
    ## zip source files to single file and make executable:
    pushd "$_temp" >> $VERBOSE;
        create_zip_archive -o "$current_dir/dist/app.zip" * -x '*__pycache__/*' -x '*.DS_Store';
    popd >> $VERBOSE;
    echo  "$PYTHON_APP_PREFIX" | cat - dist/app.zip > dist/$NAME_OF_APP;
    chmod +x "dist/$NAME_OF_APP";
    ## remove temp artefacts:
    remove_dir "$_temp";
    remove_file "dist/app.zip";
}

function run_create_artefact_go() {
    compile_go;
}

function run_main() {
    call_v_python src/main.py $@;
}

function run_main_go() {
    compile_go;
    ./dist/$NAME_OF_APP $@;
}

function run_explore_console() {
    _log_info "READY TO EXPLORE.";
    $CMD_EXPLORE;
}

function run_test_unit() {
    local asverbose=$1;
    local verboseoption="";
    ( $asverbose ) && verboseoption="-v";
    _log_info "RUN UNITTESTS";
    local output="$(call_v_utest            \
        $verboseoption                      \
        --top-level-directory "."           \
        --start-directory "${PATH_TEST}"    \
        --pattern "${UNITTEST_SCHEMA}" 2>&1 \
    )";
    _cli_message "$output";
    ( echo "$output" | grep -Eq "^[[:space:]]*(FAIL:|FAILED)" ) \
        && _log_fail "Unit tests failed!";
    _log_info "Unit tests successful!";
}

function run_test_unit_go() {
    _log_fail "Unit tests not yet implemented for go.";
}

function run_test_cases() {
    local args="$@";
    _log_info "RUN TEST CASES";
    call_v_python test/cases/main.py $args;
}

function run_test_cases_go() {
    _log_fail "Case tests not yet implemented for go.";
}

function run_clean_artefacts() {
    _log_info "CLEAN ARTEFACTS";
    garbage_collection_build;
    garbage_collection_python;
    garbage_collection_dist;
}
