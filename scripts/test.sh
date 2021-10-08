#!/usr/bin/env bash

##############################################################################
#    DESCRIPTION: Script for test-processes.
#
#    Usage:
#    ~~~~~~
#    ./test.sh [options]
##############################################################################

SCRIPTARGS="$@";
FLAGS=( $@ );
ME="scripts/test.sh";
SERVICE="test-service";

source scripts/.lib.sh;

mode="$( get_one_kwarg_space "$SCRIPTARGS" "-+mode" "")";
lang="$( get_one_kwarg_space "$SCRIPTARGS" "-+lang" "python" )";
options="$( get_kwarg "$SCRIPTARGS" "-+options" "" )";
option_venv="$( get_one_kwarg_space "$SCRIPTARGS" "-+venv" "true" )";
( $option_venv ) && use_python_venv_true || use_python_venv_false;

if [ "$mode" == "setup" ]; then
    if [ "$lang" == "go" ]; then
        run_setup_go;
    else #elif [ "$lang" == "python" ]; then
        run_setup;
    fi
elif [ "$mode" == "unit" ]; then
    if [ "$lang" == "go" ]; then
        run_test_unit_go $options;
    else #elif [ "$lang" == "python" ]; then
        run_test_unit $options;
    fi
elif [ "$mode" == "cases" ]; then
    if [ "$lang" == "go" ]; then
        run_test_cases_go $options;
    else #elif [ "$lang" == "python" ]; then
        run_test_cases $options;
    fi
elif [ "$mode" == "explore" ]; then
    run_explore_console;
else
    _log_error   "Invalid cli argument.";
    _cli_message "";
    _cli_message "  Call \033[1m./test.sh\033[0m with one of the commands";
    _cli_message "    $( _help_cli_key_values      "--mode" "         " "setup" "unit" "cases" "explore" )";
    _cli_message "    $( _help_cli_key_values      "[--lang]" "       " "go" "python" )";
    _cli_message "";
    _cli_message "    $( _help_cli_key_description "--lang python" "  " "(default) runs option for the python source code" )";
    _cli_message "    $( _help_cli_key_description "--lang go" "      " "runs option for the go source code" )";
    _cli_message "";
    _cli_message "    $( _help_cli_key_description "--mode setup" "   " "compiles programme with test configuration" )";
    _cli_message "    $( _help_cli_key_description "--mode unit" "    " "runs unit test" )";
    _cli_message "    $( _help_cli_key_description "--mode cases" "   " "runs through test cases" )";
    _cli_message "    $( _help_cli_key_description "--mode explore" " " "opens the console (potentially in docker)" )";
    _cli_message "";
    exit 1;
fi
