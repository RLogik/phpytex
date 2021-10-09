#!/usr/bin/env bash

##############################################################################
#    DESCRIPTION: Script for build-processes.
#
#    Usage:
#    ~~~~~~
#    ./build.sh [options]
##############################################################################

SCRIPTARGS="$@";
FLAGS=( $@ );
ME="scripts/build.sh";
SERVICE="prod-service";

source scripts/.lib.sh;

mode="$( get_one_kwarg_space "$SCRIPTARGS" "-+mode" "" )";
lang="$( get_one_kwarg_space "$SCRIPTARGS" "-+lang" "python" )";
options="$( get_one_kwarg_space "$SCRIPTARGS" "-+options" "" )";
option_venv="$( get_one_kwarg_space "$SCRIPTARGS" "-+venv" "true" )";
( $option_venv ) && use_python_venv_true || use_python_venv_false;

if [ "$mode" == "setup" ]; then
    if [ "$lang" == "go" ]; then
        run_setup_go;
    else #elif [ "$lang" == "python" ]; then
        run_setup;
    fi
elif [ "$mode" == "dist" ]; then
    if [ "$lang" == "go" ]; then
        run_create_artefact_go;
    else
        run_create_artefact;
    fi
elif [ "$mode" == "run" ]; then
    if [ "$lang" == "go" ]; then
        run_main_go $options;
    else #elif [ "$lang" == "python" ]; then
        run_main $options;
    fi
elif [ "$mode" == "examples" ]; then
    run_create_examples;
elif [ "$mode" == "explore" ]; then
    run_explore_console;
else
    _log_error   "Invalid cli argument.";
    _cli_message "";
    _cli_message "  Call \033[1m./build.sh\033[0m with one of the commands";
    _cli_message "    $( _help_cli_key_values      "--mode" "          " "setup" "dist" "run" "examples" "explore" )";
    _cli_message "    $( _help_cli_key_values      "[--lang]" "        " "go" "python" )";
    _cli_message "";
    _cli_message "    $( _help_cli_key_description "--lang python" "   " "(default) runs option for the python source code" )";
    _cli_message "    $( _help_cli_key_description "--lang go" "       " "runs option for the go source code" )";
    _cli_message "";
    _cli_message "    $( _help_cli_key_description "--mode setup" "    " "compiles programme" )";
    _cli_message "    $( _help_cli_key_description "--mode dist" "     " "creates distribution artefact" )";
    _cli_message "    $( _help_cli_key_description "--mode run" "      " "runs the programme" )";
    _cli_message "    $( _help_cli_key_description "--mode examples" " " "builds the examples for the repository" )";
    _cli_message "    $( _help_cli_key_description "--mode explore" "  " "opens the console (potentially in docker)" )";
    _cli_message "";
    exit 1;
fi

exit 0;
