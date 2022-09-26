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

env_from ".env" import NAME_OF_APP;

export PYTHON_APP_PREFIX=\
'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-''';

##############################################################################
# MAIN METHODS: PROCESSES
##############################################################################

function run_create_artefact() {
    local current_dir="$PWD";
    local success;
    ## create temp artefacts:
    local _temp="$( create_temporary_dir "dist" )";

    copy_dir dir="src" from="." to="$_temp";
    copy_file file="VERSION" from="dist" to="${_temp}/src/setup";
    mv "${_temp}/src/__main__.py" "$_temp";
    ## zip source files to single file and make executable:
    pushd "$_temp" >> $VERBOSE;
        ( zip -r -o "$current_dir/dist/app.zip" * -x '*__pycache__/*' -x '*.DS_Store' );
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
