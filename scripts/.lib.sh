#!/usr/bin/env bash

##############################################################################
#    DESCRIPTION: Library of methods specifically for the project.
#    Include using source .whales/.lib.sh
##############################################################################

source .whales/.lib.sh;

##############################################################################
# GLOBAL VARIABLES
##############################################################################

env_from ".env" import REQUIREMENTS_PY     as PATH_REQ_PY;
env_from ".env" import NAME_OF_APP;
env_from ".env" import IP                  as DOCKER_IP;
env_from ".env" import PORT_HOST           as DOCKER_PORT_HOST;
env_from ".env" import PORT_CONTAINER      as DOCKER_PORT_CONTAINER;
env_from ".env" import PORTS               as DOCKER_PORTS;

whales_set_ports "$DOCKER_PORTS";

export CONFIGENV="data/.env";

##############################################################################
# AUXILIARY METHODS: Zip
##############################################################################

function create_zip_archive() {
    zip -r $@;
}

##############################################################################
# AUXILIARY METHODS: Python
##############################################################################

function create_python_venv() {
    ! [ -d build ] && mkdir build;
    pushd build >> $VERBOSE;
        call_python -m venv env;
    popd >> $VERBOSE;
}

function activate_python_venv() {
    if ( is_linux ); then
        source build/env/bin/activate;
    else
        source build/env/Scripts/activate;
    fi
}

function deactivate_python_venv() {
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
    pushd src >> $VERBOSE;
        # clean_all_files_of_pattern "*\.pyo";
        clean_all_folders_of_pattern "__pycache__";
    popd >> $VERBOSE;
    pushd test >> $VERBOSE;
        # clean_all_files_of_pattern "*\.pyo";
        clean_all_folders_of_pattern "__pycache__";
    popd >> $VERBOSE;
}

##############################################################################
# MAIN METHODS: PROCESSES
##############################################################################

function run_setup() {
    _log_info "SETUP";
    _log_info "Create VENV";
    create_python_venv;
    _log_info "Check and install missing requirements";
    install_requirements_v_python "$PATH_REQ_PY";
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
    echo '#!/usr/bin/env python3' | cat - dist/app.zip > dist/$NAME_OF_APP;
    chmod +x "dist/$NAME_OF_APP";
    ## remove temp artefacts:
    remove_dir "$_temp";
    remove_file "dist/app.zip";
}

function run_main() {
    args="$@";
    call_v_python src/main.py $args;
}

function run_explore_console() {
    _log_info "READY TO EXPLORE.";
    $CMD_EXPLORE;
}

function run_test_unit() {
    local asverbose=$1;
    local verboseoption="";
    ( $asverbose ) && verboseoption="-v";
    _log_info "UNITTESTS";
    local output="$(call_v_utest            \
        $verboseoption                      \
        --top-level-directory "."           \
        --start-directory "${PATH_TEST}"    \
        --pattern "${UNITTEST_SCHEMA}" 2>&1 \
    )";
    _cli_message "$output";
    ( echo "$output" | grep -Eq "^[[:space:]]*(FAIL:|FAILED)" ) \
        && _log_fail "Unit tests failed!";
    _log_info "Unit tests erfolgreich!";
}

function run_clean_artefacts() {
    _log_info "CLEAN ARTEFACTS";
    garbage_collection_build;
    garbage_collection_python;
}
