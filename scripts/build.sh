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
options="$( get_kwarg "$SCRIPTARGS" "-+options" "" )";

if [ "$mode" == "setup" ]; then
    # whale_call <service>  <tag-sequence>    <save, it, ports> <type, command>
    whale_call   "$SERVICE" ".,setup"         true false true   SCRIPT $ME $SCRIPTARGS;
    run_setup;
elif [ "$mode" == "dist" ]; then
    # whale_call <service>  <tag-sequence>    <save, it, ports> <type, command>
    whale_call   "$SERVICE" "setup,dist"      false false true  SCRIPT $ME $SCRIPTARGS;
    run_create_artefact;
elif [ "$mode" == "run" ]; then
    # whale_call <service>  <tag-sequence>    <save, it, ports> <type, command>
    whale_call   "$SERVICE" "setup,run"       false false true  SCRIPT $ME $SCRIPTARGS;
    run_main $options;
elif [ "$mode" == "explore" ]; then
    # whale_call <service>  <tag-sequence>    <save, it, ports> <type, command>
    whale_call   "$SERVICE" "setup,(explore)" false true true   SCRIPT $ME $SCRIPTARGS;
    run_explore_console;
else
    _log_error   "Invalid cli argument.";
    _cli_message "";
    _cli_message "  Call \033[1m./build.sh\033[0m with one of the commands";
    _cli_message "    $( _help_cli_key_values      "--mode" "         " "setup" "dist" "run" "explore" )";
    _cli_message "    $( _help_cli_key_description "--mode setup" "   " "compiles programme" )";
    _cli_message "    $( _help_cli_key_description "--mode dist" "    " "creates distribution artefact" )";
    _cli_message "    $( _help_cli_key_description "--mode run" "     " "runs the programme" )";
    _cli_message "    $( _help_cli_key_description "--mode explore" " " "opens the console (potentially in docker)" )";
    _cli_message "";
    exit 1;
fi
