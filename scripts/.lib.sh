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

env_from ".env" import REQUIREMENTS_GO           as PATH_REQ_GO;
env_from ".env" import REQUIREMENTS_PY           as PATH_REQ_PY;
env_from ".env" import REQUIREMENT_ANTLR_VERSION as ANTLR_VERSION;
env_from ".env" import NAME_OF_APP;
env_from ".env" import TEST_TIMEOUT;

export CONFIGENV="data/.env";
export PATH_PROJECT_PY="python";
export PATH_PROJECT_GO="golang";
export PATH_GO_ASSETS_GRAMMAR="assets/grammars";
export PATH_GO_INTERNAL_GRAMMAR="internal/tokenisers/grammars";
export PYTHON_APP_PREFIX=\
'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-'''
export USE_VENV=false;
export UNITTEST_SCHEMA_PY="test_*.py";

##############################################################################
# AUXILIARY METHODS: Zip
##############################################################################

function create_zip_archive() {
    zip -r $@;
}

##############################################################################
# AUXILIARY METHODS: Java
##############################################################################

function call_java() {
    java -jar $@;
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
    local has_problems=false;
    local problem_packages=();

    pushd $PATH_PROJECT_GO >> $VERBOSE;
        # go mod tidy; # <- use to detect unused packages in project
        remove_file "go.sum";

        _log_info "Add go requirements";
        dos_to_unix "$cwd/$path";
        local line;
        while read line; do
            line="$( _trim_trailing_comments "$line" )";
            [ "$line" == "" ] && continue;
            _log_info "Run \033[92;1mGO GET\033[0m to install \033[93;1m$line\033[0m.";
            ( call_go get "$line" 2> $VERBOSE ) && continue;
            has_problems=true;
            problem_packages+=( "$line" );
        done <<< "$( cat "$cwd/$path" )";
    popd >> $VERBOSE

    ( $has_problems ) && _log_fail "Something went wrong whilst using \033[92;1mPIP\033[0m to install: {\033[93;1m${problem_packages[*]}\033[0m}.";
}

function compile_go() {
    local path="$1";
    local cwd="$PWD";
    pushd "$PATH_PROJECT_GO" >> $VERBOSE;
        precompile_antlr_jar "Go" "${ANTLR_VERSION}" "${PATH_GO_ASSETS_GRAMMAR}" "${PATH_GO_INTERNAL_GRAMMAR}";
    popd >> $VERBOSE;
    _log_info "Compile \033[1mmain.go\033[0m with \033[1mgolang\033[0m";
    remove_file "dist/$NAME_OF_APP";
    pushd "$path" >> $VERBOSE;
        # call_go build -o "$cwd/dist/$NAME_OF_APP" "main.go";
    popd >> $VERBOSE;
    ! [ -f "dist/$NAME_OF_APP" ] && return 1;
    return 0;
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
        _log_info "Run \033[92;1mPIP\033[0m to install \033[93;1m$line\033[0m.";
        ( call_pipinstall "$line" >> $VERBOSE ) && continue;
        has_problems=true;
        problem_packages+=( "$line" );
    done <<< "$( cat "$path" )";

    ( $has_problems ) && _log_fail "Something went wrong whilst using \033[92;1mPIP\033[0m to install: {\033[93;1m${problem_packages[*]}\033[0m}.";
}

function install_requirements_v_python() { activate_python_venv && install_requirements_python $@; }

##############################################################################
# AUXILIARY METHODS: ANLTR4
##############################################################################

function install_antlr_jar() {
    local pathAssets="$1";
    local version="$2";
    local url="http://www.antlr.org/download/antlr-${}-complete.jar";
    local fname;
    ( wget ${url} >> $VERBOSE 2> $VERBOSE ) || \
        _log_fatal "The command \033[1;2mwget ${url}\033[0m could not be carried out.\n    Please download the \033[1mantlr*.jar\033[0m file manually and move to (golang)\033[1m${pathAssets}/antlr.jar\033[0m (including rename).";
    while read fname; do
        ( [ "$fname" == "" ] || ! [ -f "$fname" ] ) && continue;
        _log_info "\033[92;1mANTLR\033[1m-${version}\033[0m was downloaded and placed in \033[1m${pathAssets}/antlr.jar\033[0m.";
        mv "$fname" "${pathAssets}/antlr.jar";
        return 0;
    done <<< "$( ls antlr*.jar 2> $VERBOSE )"
    _log_fatal "Installation of \033[1mantlr-${version}\033[0m failed.";
}

function precompile_antlr_jar() {
    local cwd="$PWD";
    local lang="$1";
    local version="$2";
    local pathAssets="$3"
    local pathInternal="$4"
    local fname;
    local name;
    local success=0;
    _log_info "Precompile grammar";
    ! [ -f "${pathAssets}/antlr.jar" ] && install_antlr_jar "${pathAssets}" "${version}";
    pushd "${pathAssets}" >> $VERBOSE;
        remove_dir_force ".antlr"; ## <- the folder .antlr may be automatically generated, but we do not need it
        while read fname; do
            ( [ "$fname" == "" ] || ! [ -f "$fname" ] ) && continue;
            name="$( echo "$fname" | sed -E "s/^(.*)\.g4$/\1/g" )";
            _log_info "Use \033[92;1mANTLR\033[0m to precompile grammar \033[1m${fname}\033[0m";
            ( call_java antlr.jar -Dlanguage=$lang "$fname" -o "$name" ) || \
                _log_fatal "Something went wrong when precompiling grammar \033[1m${fname}\033[0m!";
            mv "$name" "${cwd}/${pathInternal}";
        done <<< "$( ls *.g4 2> $VERBOSE )"
    popd >> $VERBOSE;
    return 0;
}

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

function garbage_collection_misc() {
    clean_all_folders_of_pattern ".DS_Store";
}

function garbage_collection_python() {
    clean_folder_contents "$PATH_PROJECT_PY/build";
    local path;
    for path in "$PATH_PROJECT_PY"; do
        pushd "$path" >> $VERBOSE;
            # clean_all_files_of_pattern "*\.pyo";
            clean_all_folders_of_pattern "__pycache__";
        popd >> $VERBOSE;
    done
}

function garbage_collection_go {
    clean_all_folders_of_pattern ".antlr";
}

function garbage_collection_dist() {
    remove_file "dist/$NAME_OF_APP";
}

##############################################################################
# MAIN METHODS: PROCESSES
##############################################################################

function run_setup() {
    _log_info "RUN SETUP";
    local current_dir="$PWD";
    pushd $PATH_PROJECT_PY >> $VERBOSE;
        create_python_venv;
        _log_info "Check and install missing requirements";
        install_requirements_v_python "$current_dir/$PATH_REQ_PY";
    popd >> VERBOSE;
}

function run_setup_go() {
    install_requirements_go "$PATH_REQ_GO";
}

function run_create_artefact() {
    local current_dir="$PWD";
    local success;
    ## create temp artefacts:
    local _temp="$( create_temporary_dir "dist" )";

    mkdir "$_temp/src"
    cp -r "$PATH_PROJECT_PY/src/." "$_temp/src";
    copy_file file="VERSION" from="dist" to="${_temp}/src/setup";
    mv "${_temp}/src/__main__.py" "$_temp";
    ## zip source files to single file and make executable:
    pushd "$_temp" >> $VERBOSE;
        ( create_zip_archive -o "$current_dir/dist/app.zip" * -x '*__pycache__/*' -x '*.DS_Store' );
        success=$?
    popd >> $VERBOSE;
    if [ $success -eq 0 ]; then
        echo  "$PYTHON_APP_PREFIX" | cat - dist/app.zip > dist/$NAME_OF_APP;
        chmod +x "dist/$NAME_OF_APP";
    fi
    ## remove temp artefacts:
    remove_dir "$_temp";
    remove_file "dist/app.zip";
    ! [ $success -eq 0 ] && return 1;
    _log_info "Python artefact successfully created.";
    return 0;
}

function run_create_artefact_go() {
    local current_dir="$PWD";
    local success;
    ## create temp artefacts:
    local _temp="$( create_temporary_dir "dist" )";
    cp -r "$PATH_PROJECT_GO/." "$_temp";
    copy_file file="VERSION" from="dist" to="${_temp}/assets";
    ( compile_go "$_temp" );
    success=$?;
    ## remove temp artefacts:
    remove_dir "$_temp";
    ! [ $success -eq 0 ] && return 1;
    return 0;
}

function  run_create_examples() {
    local current_dir="$PWD";
    local path;
    local sandboxpath;
    _log_info "CHECK IF ARTEFACT EXISTS";
    ! [ -f dist/$NAME_OF_APP ] && _log_fail "First run \033[1mbuild --mode dist\033[0m.";
    _log_info "Binary artefact exists.";
    _log_info "CREATE EXAMPLES";
    while read path; do
        [ "$path" == "" ] && continue;
        sandboxpath="$( echo "$path" | sed -E "s/^examples\/example_/examples\/expected_/g" )";
        [ "$path" == "$sandboxpath" ] && _log_error "Could not create example for \033[1m$path\033[0m." && continue;
        [ -d "$sandboxpath" ] && remove_dir "$sandboxpath";
        [ -d "$sandboxpath" ] && _log_error "Could not clear the output folder \033[1m$sandboxpath\033[0m." && continue;
        cp -r "$path/." "$sandboxpath";
        pushd "$sandboxpath" >> $VERBOSE;
            $current_dir/dist/$NAME_OF_APP run;
        popd >> $VERBOSE;
        # [ -f "$path" ] && remove_file "$path" >> $VERBOSE && continue;
        # [ -d "$path" ] && rm -rf "$path" && continue;
    done <<< $( find examples/example_* -mindepth 0 -maxdepth 0 2> $VERBOSE );
    return 0;
}

function run_main() {
    pushd $PATH_PROJECT_PY >> $VERBOSE;
        call_v_python src/main.py $@;
    popd >> $VERBOSE;
}

function run_main_go() {
    compile_go "$PATH_PROJECT_GO";
    ./dist/$NAME_OF_APP $@;
}

function run_explore_console() {
    _log_info "READY TO EXPLORE.";
    $CMD_EXPLORE;
}

function run_test_unit() {
    local asverbose=$1;
    local verboseoption="-v";
    local success=0;
    ! ( $asverbose ) && verboseoption="";
    _log_info "RUN UNITTESTS";
    pushd $PATH_PROJECT_PY >> $VERBOSE;
        ( call_v_utest                \
            $verboseoption                          \
            --top-level-directory "test"            \
            --start-directory "test"                \
            --pattern "${UNITTEST_SCHEMA_PY}" 2>&1  \
        );
        success=$?;
    popd >> $VERBOSE;
    [ $success -eq 1 ] && _log_fail "Unit tests failed!";
    _log_info "Unit tests successful!";
    return 0;
}

function run_test_unit_go() {
    local asverbose="$1";
    local verboseoption="-v";
    local success;
    _log_info "RUN UNITTESTS";
    ! ( $asverbose ) && verboseoption=""
    pushd $PATH_PROJECT_GO >> $VERBOSE;
        ( call_go test $verboseoption -timeout $TEST_TIMEOUT -count 1 -run "^Test[A-Z].*" "phpytex" "./..." );
        success=$?;
    popd >> $VERBOSE
    [ $success -eq 1 ] && _log_fail "Unit tests failed!";
    _log_info "Unit tests successful!";
    return 0;
}

function run_test_cases() {
    local args="$@";
    local current_dir="$PWD";
    _log_info "RUN TEST CASES";
    pushd $PATH_PROJECT_PY >> $VERBOSE;
        call_v_python test/cases.py \
            --dir "$current_dir" \
            --app "$current_dir/dist/$NAME_OF_APP" \
            --config "$current_dir/test/setup/config.yml" \
            --cases $current_dir/test/cases $args;
    popd >> $VERBOSE;
}

function run_test_cases_go() {
    local args="$@";
    local current_dir="$PWD";
    _log_info "RUN TEST CASES";
    pushd $PATH_PROJECT_GO >> $VERBOSE;
        # TODO: currently runs in python - change this to go!
        call_v_python test/cases.py \
            --dir "$current_dir" \
            --app "$current_dir/dist/$NAME_OF_APP" \
            --config "$current_dir/test/setup/config.yml" \
            --cases $current_dir/test/cases $args;
    popd >> $VERBOSE;
}

function run_clean_artefacts() {
    _log_info "CLEAN ARTEFACTS";
    garbage_collection_misc;
    garbage_collection_python;
    garbage_collection_go;
    garbage_collection_dist;
}
