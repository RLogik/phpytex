#!/bin/bash

##############################################################################
#    DESCRIPTION: Script for running programme.
#
#    Usage:
#    ~~~~~~
#    . .docker.sh
#        [--project <string>]
#        --service <string>
#        [--enter <tag>]
#        [--start [--mount|--debug]]
#        [--stop]
#        [--status]
#        [--clean] [--clean-all]
#
#    Cli options:
#    ~~~~~~~~~~~~
#    --project <string>    Name of project. (Default is extracted from .env).
#    --service <string>    Name of service.
#    --enter <string>      (requires --service) Tag name. Enters docker container at <image>:tag,
#                            where <image> is automatically computed from service.
#    --start               (requires --service) Builds docker service main.
#    --stop                (requires --service) Stops all docker containers.
#    --status              (requires --service) Gets status of all containers and images.
#    --clean               (requires --service) Removes container + images bar base.
#    --clean-all           !!! warning !!! removes ALL docker containers + images, incl. project unrelated ones.
##############################################################################

SCRIPTARGS="$@";

source .whales/.lib.sh;

project="$( get_one_kwarg_space "$SCRIPTARGS" "-+project" "$WHALES_PROJECT_NAME" )";
service="$( get_one_kwarg_space "$SCRIPTARGS" "-+service" )";
tags="$(    get_one_kwarg_space "$SCRIPTARGS" "-+enter"   )";
force=false;
( has_arg "$SCRIPTARGS" "-+force" ) && force=true;

if ( has_arg "$SCRIPTARGS" "-+enter" ); then
    run_docker_enter "$project" "$service" "$tags";
elif ( has_arg "$SCRIPTARGS" "-+(start|up)" ); then
    run_docker_build "$project" "$service";
elif ( has_arg "$SCRIPTARGS" "-+(stop|down)" ); then
    run_docker_stop_down "$project" "$service";
elif ( has_arg "$SCRIPTARGS" "-+prune" ); then
    run_docker_clean $force false "$project" "$service";
    run_docker_prune;
elif ( has_arg "$SCRIPTARGS" "-+clean" ); then
    run_docker_clean $force true "$project" "$service";
    run_docker_prune;
elif ( has_arg "$SCRIPTARGS" "-+clean-all" ); then
    run_docker_clean_all $force;
elif ( has_arg "$SCRIPTARGS" "-+(status|state)" ); then
    get_docker_state "$project" "$service";
else
    _log_error   "Invalid cli argument.";
    _cli_message "";
    _cli_message "  Call \033[1m./.whales/docker.sh\033[0m with the command";
    _cli_message "    $( _help_cli_key_description "--clean-all" "     " "Cleans + prunes all docker images and containers after prompt." )";
    _cli_message "  or";
    _cli_message "    $( _help_cli_key_description "--project" "       " "<string> Name of project. (Left empty defaults to value in .env file.)" )";
    _cli_message "    $( _help_cli_key_description "--service" "       " "<string> Name of service in docker-compose.yml." )";
    _cli_message "  + one of the following commands:";
    _cli_message "      $( _help_cli_key_description "--enter" "         " "<string> ‘Tag name’ (=label \"${WHALES_LABEL_PREFIX}tag\") of docker image to be entered interactively." )";
    _cli_message "      $( _help_cli_key_description "--start/up" "      " "Starts container associated with project + service." )";
    _cli_message "      $( _help_cli_key_description "--stop/down" "     " "Stops container associated with project + service." )";
    _cli_message "      $( _help_cli_key_description "--status/state" "  " "Displays status of containers + images associated with project + service." )";
    _cli_message "      $( _help_cli_key_description "--clean" "         " "After prompt, removes all containers + images associated with project + service." )";
    _cli_message "      $( _help_cli_key_description "--prune" "         " "Like --clean but *initial* container + image are retained." )";
    _cli_message "      $( _help_cli_key_description "--force" "         " "When used with --clean-all, --clean, --prune, will skip prompts." )";
    _cli_message "";
    exit 1;
fi
