#!/bin/bash

##############################################################################
#    DESCRIPTION: Library for extraction of global vars from environment.
##############################################################################

##############################################################################
# MAIN METHODS: .env
##############################################################################

function env_value() {
    [ -f "$1" ] && source "$1" && echo "${!2}";
}

function env_required() {
    ! [ -f "$1" ] && echo -e "[\033[91mERROR\033[0m] Could not find environment file \033[1m$1\033[0m!" >> /dev/stderr && exit 1;
    source "$1";
    local value="${!2}";
    [ "$value" == "" ] && echo -e "[\033[91mERROR\033[0m] Argument \033[93;1m$2\033[0m not found in \033[1m$1\033[0m!" >> /dev/stderr && exit 1;
    echo "$value";
}

function env_from() {
    local arguments=( "$@" );
    local path="${arguments[0]}";
    local key_from="${arguments[2]}";
    local key_to="${key_from}";
    ( echo "${arguments[3]}" | grep -Eiq "^as$" ) && key_to="${arguments[4]}";
    ! ( echo "$key_to" | grep -Eiq "^([[:alpha:]]|_)([[:alpha:]]|_|[[:digit:]])*$" ) && echo -e "[\033[91mERROR\033[0m] Key argument \"\033[1m$key_to\033[0m\" not a valid name for a variable!" >> /dev/stderr && exit 1;
    local value="$( env_required "$path" "$key_from" )";
    [ "$value" == "" ] && exit 1;
    export $key_to="$value";
}

##############################################################################
# GLOBAL VARIABLES:
##############################################################################

# NOTE: do not use /bin/bash. Results in error under Windows.  Use \/bin\/bash, bash, sh -c bash, or sh.
export CMD_EXPLORE="bash";
# periodic waiting time to check a process;
export WAIT_PERIOD_IN_SECONDS=1;
export PENDING_SYMBOL="#";

env_from ".env" import CONSOLE_OUT                 as OUT;
env_from ".env" import CONSOLE_ERR                 as ERR;
env_from ".env" import CONSOLE_VERBOSE             as VERBOSE;
env_from ".env" import CONSOLE_PATH_LOGS           as PATH_LOGS;
env_from ".env" import CONSOLE_FILENAME_LOGS_DEBUG as FILENAME_LOGS_DEBUG;

export LOGGINGPREFIX="";
