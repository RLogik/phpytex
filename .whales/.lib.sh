#!/bin/bash

##############################################################################
#    DESCRIPTION: Library of methods for Whales
#    Include using source .whales/.lib.sh
##############################################################################

source .whales/.lib.globals.sh;
source .whales/.lib.utils.sh;
source .whales/.lib.docker.sh;
source .whales/.lib.meta.sh

##############################################################################
# MAIN PROCESSES FOR WHALES
##############################################################################

function run_docker_build() {
    local project="$1";
    local service="$2";
    run_docker_compose_build "$project" "$service";
}

function run_docker_stop_down() {
    local project="$1";
    local service="$2";
    run_docker_compose "$project" stop "$service";
    run_docker_compose "$project" down "$service";
}

function run_docker_prune() {
    # Prune images not used by containers and any dangling images.
    # DEV-NOTE: do not use -a flag, as this will remove images from other projects!
    docker image prune --force;
}

function run_docker_clean() {
    local force=$1;
    local include_init=$2;
    local project="$3";
    local service="$4";
    local answer;

    if ! ( $force ); then
        if ( $include_init ); then
            _log_warn "Docker containers + images associated with project/service will be removed.";
        else
            _log_warn "Docker containers + images associated with project/service (excluding initial container + image) will be removed.";
        fi
        _cli_ask "Do you wish to proceed? (y/n) ";
        read answer;
        ! ( check_answer "$answer" ) && _log_info "SKIPPING" && return;
    fi

    _cli_message "";
    _cli_message "\033[94;1mCONTAINERS\033[0m:";
    docker_remove_some_containers $include_init "$project" "$service";
    _cli_message "\033[94;1mIMAGES\033[0m:";
    docker_remove_some_images $include_init "$project" "$service";
    _cli_message "";
}

function run_docker_clean_all() {
    local force=$1;
    local answer;

    if ! ( $force ); then
        _log_warn "ALL docker containers and images will be stopped and removed. That includes containers not related to this project.";
        _cli_ask "Do you wish to proceed? (y/n) ";
        read answer;
        ! ( check_answer "$answer" ) && _log_info "SKIPPING" && return;
    fi

    _log_info "STOP AND REMOVE ALL CONTAINERS";
    docker_remove_all_containers;
    _log_info "REMOVE ALL CONTAINERS";
    docker_remove_all_images;
    _cli_message "";
}

function get_docker_state() {
    local project="$1";
    local service="$2";

    _cli_message "";
    _cli_message "\033[94;1mCONTAINERS\033[0m:";
    docker_show_states containers true "$project" "$service";
    _cli_message "";
    _cli_message "\033[94;1mIMAGES\033[0m:";
    docker_show_states images     true "$project" "$service";
    _cli_message "";
}

function run_docker_enter() {
    local service="$1";
    local tags="$2";

    [ "$tags" == "" ] && tags=".,($WHALES_DOCKER_TAG_EXPLORE)";
    whale_call "$service" "$tags" false true true;
}
