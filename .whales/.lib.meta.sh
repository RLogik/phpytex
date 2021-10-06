#!/bin/bash

##############################################################################
#    DESCRIPTION: Library of methods for Whales
#    Include using source .whales/.lib.meta.sh
##############################################################################

##############################################################################
# DECORATOR: whale_call
##############################################################################

####
# Checks if in docker, and either
# returns to script, or starts docker and calls script within docker.
#
# Usage:
#    whale_call <service> <tag-sequence> <save, it, ports> <type> [<script, params> / <command>]
#
# Arguments:
#    service <string>   The name of the service in docker-compose.yml.
#    tag-seq <string>   Comma separated sequence of tags,
#                         starting from the image-tag of the service
#                         potentially going through intermediate stages,
#                         ending with the desired image-tag to be applied when saving.
#                       ~> "tagStart" is taken to be the latest possible tag in the list,
#                          for which an image exists.
#                       ~> "tagFinal" is taken to be the final tag in the list.
#    save <bool>        Whether the created image is to be saved after creation
#                         / after interactive container containing image is exitted.
#    it <bool>          Whether the container is to be run interactive mode.
#    ports <bool>       Whether ports are to be exposed.
#    type   <string>    Either SCRIPT or CMD (not case sensitive).
#  Optional:
#    if type == SCRIPT, use
#       <script, params>  Name of script followed by CLI params.
#    else use
#       <command>         The full command to be carried out (within the docker context).
####
function whale_call() {
    # If whales is deactivate, ignore whale_call!
    ! ( is_whales_active ) && return 0;

    local metaargs=( "$@" );
    local service="${metaargs[0]}";
    local tags="${metaargs[1]}";
    local save=${metaargs[2]};
    local it=${metaargs[3]};
    local expose=${metaargs[4]};
    local type="$( to_lower "${metaargs[5]}" )";

    # If already inside docker:
    if ( is_docker ); then
        # If type==script, return to script, else carry out commmand:
        [ "$type" == "script" ] && return 0 || ( "${metaargs[@]:6}" ) && return 0 || return 1;
    else
        ## CHECK VALIDITY OF ARGUMENTS:
        [ ${#metaargs[@]} -lt 6 ] && _log_fail "In whales decorator \033[1mcall_within_docker\033[0m not enough arguments passed.";

        ## CREATE SERVICE:
        _log_info "YOU ARE OUTSIDE THE DOCKER ENVIRONMENT.";
        # If the tag sequence contains ".", then force start if not already up:
        local contains_init=false;
        docker_tagsequence_contains_init "$tags" && contains_init=true;
        get_docker_service "$service" $contains_init \
            || _log_fail "Could not find an existing image with one of the tags in {\033[1m$tags\033[0m} for the service \033[1m$service\033[0m.";

        ## DETERMINE ENTRY + EXIT IMAGES:
        local output=( $( docker_tagsequence_get_start_and_end "$service" "$tags" 2> $VERBOSE ) );
        local tagStart="${output[0]}";
        local tagFinal="${output[1]}";
        [ "$tagStart" == "" ] && _log_fail "Could not find a starting point for the tag-sequence {\033[1m$tags\033[0m} for the service \033[1m$service\033[0m.";
        local save_arg="";
        ( $save ) && save_arg="--save \"$tagFinal\"";

        ## DETERMINE COMMAND TO BE CALLED IN DOCKER CONTAINER:
        local cmd_arg="";
        if [ "$type" == "script" ]; then
            local script="${metaargs[6]}";
            local params="${metaargs[@]:7}";
            command="source $script $params";
            # alternative: "--command \"cat $script | dos2unix | bash -s -- $params\"";
            ! [ "$script" == "" ] && cmd_arg="--command \"$command\"";
        else
            local command="${metaargs[@]:6}";
            ! [ "$command" == "" ] && cmd_arg="--command \"$command\"";
        fi

        ## RUN SCRIPT COMMAND WITHIN DOCKER:
        whales_enter_docker --service "$service" --enter "$tagStart" $save_arg --it $it --expose $expose $cmd_arg;
        local success=$?;

        ## If type==script, do not return to script:
        [ "$type" == "script" ] && exit $success || return $success;
    fi
}

##############################################################################
# METHOD: whales_enter_docker
##############################################################################

####
# This method starts container from a specified image,
# performs a command, and then saves to a specified image.
# The following relations hold/are forced between the images:
#
#    service image
#    \____> ...
#             \____> entry image (or == service image)
#                  \
#      [ after container finished ]
#                   \________> save image
#
# Usage:
#    enter_docker
#        --service <name> --enter <tag> [--save [<tag>]]
#        --it <bool> --expose <bool>
#        [--command <string>]
#
# Flags:
#    --service <string>      The name of the service in docker-compose.yml.
#    --enter   <tag>         If argument left empty, will overwrite original.
#    [--save  [<tag>]]       If used, will save the container to an image upon completion.
#                              (Default: coincides with --entry)
#    --it <bool>             Whether or not to run docker container interactive mode.
#      false (default)         Docker will run discretely and logs will be followed.
#    --expose <bool>         Whether or not ports are to be exposed.
#                              (Default: coincides with --it)
#    [--command <string>]    Use to start container with a command.
#                              (Default: "bash")
####
function whales_enter_docker() {
    local metaargs="$@";
    local service="$(  get_one_kwarg_space "$metaargs" "-+service" ""          )";
    local save=false;
    ( has_arg "$metaargs" "-+save" ) && save=true;
    local tagStart="$( get_one_kwarg_space "$metaargs" "-+enter"   "."         )";
    local tagFinal="$( get_one_kwarg_space "$metaargs" "-+save"    "$tagStart" )";
    local it=$(        get_one_kwarg_space "$metaargs" "-+it"      "false"     );
    local expose=$(    get_one_kwarg_space "$metaargs" "-+expose"  ""          );
    local command="$(  get_one_kwarg_space "$metaargs" "-+command" ""          )";
    local command_descr="####"; # <- censore description of command.

    _log_info "ENTER DOCKER ENVIRONMENT.";
    ## Get container of service (in order to connect mounted volumes):
    # DEV-NOTE: Do not enclose in ( ... ) here, otherwise exports do not work.
    get_docker_service "$service" false;

    ## Get image_id for entry point:
    local init=false;
    [ "$tagStart" == "." ] && init=true;
    local output=( $( docker_get_service_image_from_tag $init "$service" "$tagStart" 2> $VERBOSE ) );
    local image_id="${output[0]}";
    local identifier="image with label \033[1m${WHALES_LABEL_PREFIX}tag=$tagStart\033[0m for service \033[93;1m$service\033[0m";
    ( $init ) && identifier="image for service \033[1m$service\033[0m";
    [ "$image_id" == "" ] \
        && _log_error "In whales method \033[1menter_docker\033[0m could not find $identifier!" \
        && return 1;

    _log_info "CONTINUE WITH IMAGE \033[1m$tagStart\033[0m (\033[93;1m$image_id\033[0m).";

    ## Set arguments, if empty:
    [ "$expose" == ""  ] && expose=$it;
    [ "$command" == "" ] && command="$WHALES_DOCKER_CMD_EXPLORE" && it=true;

    ## Set ports command (requires user to have called 'set ports')
    local ports_option="";
    ( $expose ) && ports_option="$WHALES_PORTS_OPTIONS";

    ################################
    # ENTER DOCKER: create container and run command
    local container_tmp="$( docker_create_unused_tmpcontainer_name )";
    _log_info "START TEMPORARY CONTAINER \033[92;1m$container_tmp\033[0m.";
    if ( $it ); then
        _log_info "EXECUTE COMMAND {\033[93;1m$command_descr\033[0m} INTERACTIVELY.";
        docker run --name="$container_tmp"                    \
            $ports_option                                     \
            --volumes-from=$WHALES_DOCKER_CONTAINER_ID:rw     \
            --label ${WHALES_LABEL_PREFIX}project="$WHALES_PROJECT_NAME" \
            --label ${WHALES_LABEL_PREFIX}service="$service"             \
            --label ${WHALES_LABEL_PREFIX}tag="$tagFinal"                \
            --label ${WHALES_LABEL_PREFIX}initial=false                  \
            -it $image_id bash -c "$command";
    else
        _log_info "EXECUTE COMMAND {\033[93;1m$command_descr\033[0m} NON-INTERACTIVELY.";
        docker run --name="$container_tmp"                    \
            $ports_option                                     \
            --volumes-from=$WHALES_DOCKER_CONTAINER_ID:rw     \
            --label ${WHALES_LABEL_PREFIX}project="$WHALES_PROJECT_NAME" \
            --label ${WHALES_LABEL_PREFIX}service="$service"             \
            --label ${WHALES_LABEL_PREFIX}tag="$tagFinal"                \
            --label ${WHALES_LABEL_PREFIX}initial=false                  \
            -d $image_id bash -c "$command";
        docker logs --follow $container_tmp;
    fi
    _log_info "WAIT FOR CONTAINER \033[92;1m$container_tmp\033[0m TO STOP.";
    _log_info "TEMPORARY CONTAINER \033[92;1m$container_tmp\033[0m TERMINATED.";
    wait_for_container_to_stop "$container_tmp";
    # EXIT DOCKER
    ################################

    ## Save state upon exit:
    if ( $save ); then
        if [[ "$tagFinal" == "." ]]; then
            # prevent saving to initial service image
            _log_warn "CANNOT OVERWRITE INITIAL IMAGE! -> SKIPPING SAVE-STATE.";
        elif [[ "$tagFinal" == "$tagStart" ]]; then
            _log_info "SAVE STATE TO \033[92;1m$tagFinal\033[0m (OVERWRITES TAGS).";
            docker commit "$container_tmp" $WHALES_DOCKER_IMAGE_NAME:$tagFinal >> $VERBOSE;
        else
            _log_info "SAVE STATE TO \033[92;1m$tagFinal\033[0m.";
            docker commit "$container_tmp" $WHALES_DOCKER_IMAGE_NAME:$tagFinal >> $VERBOSE;
        fi
    fi
    docker_remove_container "$container_tmp" 2> $VERBOSE >> $VERBOSE;
    _log_info "TEMPORARY CONTAINER \033[92;1m$container_tmp\033[0m REMOVED.";
}
