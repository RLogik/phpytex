#!/bin/bash

##############################################################################
#    DESCRIPTION: Library for extraction of global vars from environment.
#    Include using source .whales/.lib.globals.sh
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

# extraction from environments:
env_from ".whales.env" import WHALES_SETUP_PATH;
env_from ".whales.env" import WHALES_PROJECT_NAME;

export WHALES_LABEL_PREFIX="org.whales.";
export WHALES_LABEL_PREFIX_REGEX="^org\.whales\.";
export WHALES_DOCKER_COMPOSE_YML=".whales.docker-compose.yml";
export WHALES_FILE_WHALES_STATE="$WHALES_SETUP_PATH/WHALES_STATE";
export WHALES_FILE_DOCKER_STATE="$WHALES_SETUP_PATH/DOCKER_STATE";
export WHALES_TEMPCONTAINER_SCHEME_PREFIX="temp_${WHALES_PROJECT_NAME}";
export WHALES_DOCKER_TAG_EXPLORE="explore";
export WHALES_DOCKER_SERVICE="";      # NOTE: This get changed dynamically.
export WHALES_DOCKER_IMAGE_NAME="";   # ""
export WHALES_DOCKER_IMAGE_ID="";     # ""
export WHALES_DOCKER_CONTAINER_ID=""; # ""
# NOTE: do not use /bin/bash. Results in error under Windows.  Use \/bin\/bash, bash, sh -c bash, or sh.
export WHALES_DOCKER_CMD_EXPLORE="bash";
export WHALES_PORTS_OPTIONS="";

env_from "$WHALES_SETUP_PATH/logging.env" import CONSOLE_OUT                 as OUT;
env_from "$WHALES_SETUP_PATH/logging.env" import CONSOLE_ERR                 as ERR;
env_from "$WHALES_SETUP_PATH/logging.env" import CONSOLE_VERBOSE             as VERBOSE;
env_from "$WHALES_SETUP_PATH/logging.env" import CONSOLE_PATH_LOGS           as PATH_LOGS;
env_from "$WHALES_SETUP_PATH/logging.env" import CONSOLE_FILENAME_LOGS_DEBUG as FILENAME_LOGS_DEBUG;

export LOGGINGPREFIX="";
