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

if [ "$mode" == "setup" ]; then
    # whale_call <service>  <tag-sequence>    <save, it, ports> <type, command>
    whale_call   "$SERVICE" ".,setup"         true false true   SCRIPT $ME $SCRIPTARGS;
    run_setup;
elif [ "$mode" == "unit" ]; then
    # whale_call <service>  <tag-sequence>    <save, it, ports> <type, command>
    whale_call   "$SERVICE" "setup,unit"      false false true  SCRIPT $ME $SCRIPTARGS;
    run_test_unit;
elif [ "$mode" == "explore" ]; then
    # whale_call <service>  <tag-sequence>    <save, it, ports> <type, command>
    whale_call   "$SERVICE" "setup,(explore)" true true true    SCRIPT $ME $SCRIPTARGS;
    run_explore_console;
else
    _log_error   "Invalid cli argument.";
    _cli_message "";
    _cli_message "  Call \033[1m./test.sh\033[0m with one of the commands";
    _cli_message "    $( _help_cli_key_values      "--mode" "         " "setup" "unit" "explore" )";
    _cli_message "    $( _help_cli_key_description "--mode setup" "   " "compiles programme with test configuration" )";
    _cli_message "    $( _help_cli_key_description "--mode unit" "    " "runs unit test" )";
    _cli_message "    $( _help_cli_key_description "--mode explore" " " "opens the console (potentially in docker)" )";
    _cli_message "";
    exit 1;
fi
