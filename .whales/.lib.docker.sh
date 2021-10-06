#!/bin/bash

##############################################################################
#    DESCRIPTION: Library of methods for Whales
#    Include using source .whales/.lib.whales.sh
##############################################################################

##############################################################################
# AUXILIARY METHODS: BASIC
##############################################################################

function run_docker_compose() {
    local project="$1";
    local args=( "$@" );
    local config="$WHALES_DOCKER_COMPOSE_YML";
    docker-compose --file "$config" --project-name "$project" ${args[@]:1};
}

function run_docker_compose_build() {
    local project="$1";
    local service="$2";
    local path="$WHALES_SETUP_PATH";

    clean_scripts_dos2unix "$path";
    _log_info "START DOCKER SERVICE \033[92;1m$service\033[0m.";
    run_docker_compose "$project" build \
        --build-arg WHALES_SETUP_PATH=$path \
        --build-arg WHALES_PROJECT_NAME=$project \
        --build-arg WHALES_SELECTED_SERVICE=$service \
        "$service";
}

function docker_create_unused_name() {
    local name="$1";
    local k=0;
    while ( docker ps -aq --format '{{.Names}}' | grep -Eq "^${name}_${k}$" ); do k=$(( $k + 1 )); done;
    echo "${name}_${k}";
}

function docker_create_unused_container_name_for_service() {
    local service="$1"
    echo "$( docker_create_unused_name "${WHALES_PROJECT_NAME}_${service}" )";
}

function docker_create_unused_tmpcontainer_name() {
    echo "$( docker_create_unused_name "${WHALES_TEMPCONTAINER_SCHEME_PREFIX}" )";
}

##############################################################################
# AUXILIARY METHODS: MISC
##############################################################################

function get_tag_from_image_name() {
    local value="$1";
    local pattern="^.*:([^:]*)$";
    ! ( echo "$value" | grep -Eq "$pattern" ) && echo "<none>" && return;
    echo "$( echo "$1" | sed -E "s/$pattern/\1/g" )";
}

function get_whales_dockerlabels() {
    local id="$1";
    local labels="$( docker inspect --format '{{ json .Config.Labels }}' "$id" )";
    ! ( echo "$labels" | grep -Eq "^\{.*\}$" ) && return;
    if ( check_jq_exists ); then
        local regex="${WHALES_LABEL_PREFIX_REGEX//\\/\\\\}.+";
        local selector=".key | match(\"$regex\"; \"g\")";
        local format=".key + \" \" + (.value|tostring)";
        echo "$labels" |  jq -r "to_entries | map(select($selector) | $format) | .[]";
    else
        local line;
        while read line; do
            [ "$line" == "" ] && break;
            local parts=( $line );
            local key="${parts[0]}";
            ( echo "$key" | grep -Eiq "${WHALES_LABEL_PREFIX_REGEX}" ) && echo "$line";
        done <<< "$( json_dictionary_kwargs "$labels"  )";
    fi
}

##############################################################################
# AUXILIARY METHODS: SERVICES, CONTAINERS, IMAGES
##############################################################################

function docker_get_service_image_ids() {
    local project="$1";
    local service="$2";
    local format="{{.ID}}";
    local filters="";
    ! [ "$project" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}project=$project";
    ! [ "$service" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}service=$service";
    docker images -aq --format "$format" $filters;
}

function docker_get_service_container_ids() {
    local project="$1";
    local service="$2";
    local format="{{.ID}}";
    local filters="";
    ! [ "$project" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}project=$project";
    ! [ "$service" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}service=$service";
    docker ps -aq --format "$format" $filters;
}

function docker_get_container_id_from_image_id() {
    local image_id="$1";
    local format="{{.Image}}"; # <- DEV-NOTE: scheme in table for image_id is /sha:.*/
    local pattern="(^|^[^:]*:)$image_id";
    local line;
    while read line; do
        line="$( _trim "$line" )";
        [ "$line" == "" ] && continue;
        local container_id="$line";
        local value="$( docker inspect --format="$format" "$container_id" )";
        ( echo "$value" | grep -Eq "$pattern" ) && echo "$container_id" && return;
    done <<< "$( docker ps -aq --format '{{.ID}}' )";
    _log_fail "Could not find \033[1mcontainer\033[0m for image_id \033[93;1m$image_id\033[0m.";
}

function docker_get_service_image_from_tag() {
    local init=$1;
    local project="$WHALES_PROJECT_NAME";
    local service="$2";
    local value="$3";
    local format="{{.ID}}\t{{.Repository}}\t{{.Tag}}";
    local filters="--filter label=${WHALES_LABEL_PREFIX}project=$project --filter label=${WHALES_LABEL_PREFIX}service=$service";
    if ( $init ); then
        filters="$filters --filter label=${WHALES_LABEL_PREFIX}initial=true";
    else
        filters="$filters --filter label=${WHALES_LABEL_PREFIX}tag=$value";
    fi
    local lines="$( docker images -aq --format "$format" $filters )";
    local line;
    while read line; do
        line="$( _trim "$line" )";
        [ "$line" == "" ] && continue;
        local columns=( $line );
        local image_id="${columns[0]}";
        local image="${columns[1]}";
        local tag="${columns[2]}";
        ( echo "$image:$tag" | grep -Eiq "<none>" ) && echo "$image_id" || echo "$image_id $image $tag";
        return;
    done <<< "$lines";
    if ( $init ); then
        _log_fail "Could not find initial image of service \033[1m$service\033[0m!";
    else
        _log_fail "Could not find image with tag \033[1m$value\033[0m for service \033[1m$service\033[0m!";
    fi
}

function docker_exists_service_tag() {
    local service="$1";
    local value="$2";
    local init=false;
    [ "$value" == "." ] && init=true;
    [ "$value" == "" ] && return 1;
    local output=( $( docker_get_service_image_from_tag $init "$service" "$value" 2> $VERBOSE ) );
    local image_id="${output[0]}";
    [ "$image_id" == "" ] && return 1 || return 0;
}

function docker_set_service_image() {
    local project="$WHALES_PROJECT_NAME";
    local service="$1";
    local output=( $( docker_get_service_image_from_tag true "$service" "." 2> $VERBOSE ) );
    local image_id="${output[0]}";
    local image="${output[1]}";
    [ "$image_id" == "" ] && _log_error "There is no image associated to the service \033[1m$service\033[0m." && return 1;
    [ "$image" == "" ] && name="${project}_${service}"
    export WHALES_DOCKER_IMAGE_NAME="$image";
    export WHALES_DOCKER_IMAGE_ID="$image_id";
}

function docker_set_service_container() {
    local project="$WHALES_PROJECT_NAME";
    local service="$1";
    local image_id="$WHALES_DOCKER_IMAGE_ID";
    [ "$image_id" == "" ] && _log_error "Could not find container associated to service \033[1m$service\033[0m!" && return 1;
    local container_id="$( docker_get_container_id_from_image_id "$image_id" 2> $VERBOSE )";
    [ "$container_id" == "" ] && _log_error "There is no container associated to the service \033[1m$service\033[0m." && return 1;
    export WHALES_DOCKER_CONTAINER_ID="$container_id";
}

function docker_tagsequence_preformat() {
    local tags="$1";
    # strip spaces:
    tags="$( echo "$tags" | sed -E s/[[:space:]]//g )";
    # for sequences "tag_1" of length one, replace by "tag_1,tag_1"
    ! ( echo "$tags" | grep -Eq "," ) && tags="$tags,$tags";
    # remove all occurrences of ",,":
    tags="$( echo "$tags" | sed -E "s/,,+/,/g" )";
    # replace sequences of the form ",tag_1,...,tag_n" by ".,tag_1,...,tag_n"
    tags="$( echo "$tags" | sed -E "s/^,(.+)$/.,\1/" )";
    # replace all occurrences of "...,(tag),..." with "...,tag,tag,...":
    tags="$( echo "$tags" | sed -E "s/\(([^\)]*)\)/\1,\1/g" )";
    echo "$tags";
}

function docker_tagsequence_contains_init() {
    local tags="$( docker_tagsequence_preformat "$1" )";
    local tagParts=( ${tags//","/" "} );
    local nTags=${#tagParts[@]};
    local i=0;
    for (( i=0; i < $nTags - 1; i++ )); do
        local tag="${tagParts[$i]}";
        [ "$tag" == "." ] && return 0;
    done
    return 1;
}

function docker_tagsequence_get_start_and_end() {
    local service="$1";
    local tags="$( docker_tagsequence_preformat "$2" )";
    local tagParts=( ${tags//","/" "} );
    local nTags=${#tagParts[@]};
    local tagStart="";
    local tagFinal="";
    local i=0;
    for (( i=$nTags-1; i >= 0; i-- )); do
        local tag="${tagParts[$i]}";
        # Do not allow position n-1 to be used as a start tag:
        (( $i == $nTags - 1 )) && tagFinal="$tag" && continue;
        # If tag exists as entry point, then stop search:
        ( docker_exists_service_tag "$service" "$tag" ) && echo "$tag $tagFinal" && return;
    done
    _log_fail "Could not find a starting point.";
}

##############################################################################
# AUXILIARY METHODS: STATE
##############################################################################

function docker_is_container_stopped() {
    local id="$1";
    container_is_running="$( docker container inspect --format '{{.State.Running}}' $id 2> $VERBOSE || echo "" )";
    container_state="$(      docker container inspect --format '{{.State.Status}}'  $id 2> $VERBOSE || echo "" )";
    ## if empty status, then container does not exist --> "stopped":
    if [ "$container_is_running" == "" ] && [ "$container_state" == "" ]; then return 0; fi
    ## else check values:
    [ "$container_is_running" == "false" ] && return 0 || return 1;
    [ "$container_state" == "exited" ] && return 0 || return 1;
}

function wait_for_container_to_stop() {
    local name="$1";
    local displayed=false;
    ## TODO: implement `show_progressbar`?
    # tput civis; # cursor invisible
    while ! ( docker_is_container_stopped "$name" ); do
        if ! ( $displayed ); then
            _log_info "pending... $PENDING_SYMBOL" true;
        else
            _cli_trailing_message "$PENDING_SYMBOL";
        fi
        displayed=true;
        sleep $WAIT_PERIOD_IN_SECONDS;
    done
    # tput cnorm; # cursor visible
    ( $displayed ) && _cli_trailing_message "\n";
}

function docker_show_states() {
    local part="$1";
    local show_labels=$2;
    local project="$3";
    local service="$4";
    local filters="";
    ! [ "$project" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}project=$project";
    ! [ "$service" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}service=$service";
    local format="";
    if [[ "$part" == "images" ]]; then
        format="table {{.ID}}\t{{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}";
    elif [[ "$part" == "containers" ]]; then
        format="table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.State}}\t{{.Ports}}\t{{.Size}}\t{{.CreatedAt}}";
    else
        _log_fail "Usage \033[1mdocker_show_states images|containers <show_labels> <project> <service>\033[0m.";
    fi
    if ( $show_labels ); then
        local lines="";
        if [[ "$part" == "images" ]]; then
            lines="$( docker images -aq --format "$format" $filters )";
        elif [[ "$part" == "containers" ]]; then
            lines="$( docker ps -aq --format "$format" $filters )";
        fi
        local first_line=true;
        local line;
        _cli_message " ________________";
        _cli_message "|";
        while read line; do
            line="$( _trim "$line" )";
            [ "$line" == "" ] && break;
            ( $first_line ) && _cli_message "| \033[94;1m$line\033[0m" && first_line=false && continue;
            _cli_message "|____";
            _cli_message "| $line";
            local parts=( $line );
            local id="${parts[0]}";
            local first_label_line=true;
            local kwarg;
            while read kwarg; do
                if ( $first_label_line ); then
                    first_label_line=false;
                    _cli_message "|      labels:   $kwarg";
                else
                    _cli_message "|                $kwarg";
                fi
            done <<< "$( get_whales_dockerlabels "$id" )";
        done <<< "$lines";
        _cli_message "|________________";
    else
        _cli_message " ________________";
        if [[ "$part" == "images" ]]; then
            docker images -aq --format "$format" $filters;
        elif [[ "$part" == "containers" ]]; then
            docker ps -aq --format "$format" $filters;
        fi
        docker ps -aq --format "$format" $filters;
        _cli_message "________________";
    fi
}

##############################################################################
# AUXILIARY METHODS: CLEANING
##############################################################################

function docker_remove_container() {
    local container="$1";
    docker stop "$container" && docker rm "$container";
}

function docker_remove_image() {
    local image="$1";
    docker rmi -f "$image";
}

function docker_remove_some_containers() {
    local include_init=$1;
    local project="$2";
    local service="$3";
    local filters="";
    ! [ "$project" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}project=$project";
    ! [ "$service" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}service=$service";
    ! ( $include_init ) && filters="$filters --filter label=${WHALES_LABEL_PREFIX}initial=false";
    local format="{{.ID}}";
    local lines="$( docker ps -aq --format "$format" $filters )";
    local found=false;
    local line;
    while read line; do
        line="$( _trim "$line" )";
        [ "$line" == "" ] && continue;
        found=true;
        id="$line";
        docker_remove_container "$id" 2> $VERBOSE >> $VERBOSE \
            && _cli_message "Removed \033[1mcontainer\033[0m with id {\033[1m$id\033[0m}." \
            || _log_error "Could not remove \033[1mcontainer\033[0m with id {\033[1m$id\033[0m}.";
    done <<< "$lines";
    ! ( $found ) && _cli_message "No containers were removed.";

}

function docker_remove_some_images() {
    local include_init=$1;
    local project="$2";
    local service="$3";
    local filters="";
    ! [ "$project" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}project=$project";
    ! [ "$service" == "" ] && filters="$filters --filter label=${WHALES_LABEL_PREFIX}service=$service";
    ! ( $include_init ) && filters="$filters --filter label=${WHALES_LABEL_PREFIX}initial=false";
    local format="{{.ID}}";
    local lines="$( docker images -aq --format "$format" $filters )";
    local found=false;
    local line;
    while read line; do
        line="$( _trim "$line" )";
        [ "$line" == "" ] && continue;
        found=true;
        id="$line";
        docker_remove_image "$id" 2> $VERBOSE >> $VERBOSE \
            && _cli_message "Removed \033[1mimage\033[0m with id {\033[1m$id\033[0m}." \
            || _log_error "Could not remove \033[1mimage\033[0m with id {\033[1m$id\033[0m}.";
    done <<< "$lines";
    ! ( $found ) && _cli_message "No images were removed.";
}

function docker_remove_all_containers() {
    local line;
    while read line; do
        line="$( _trim "$line" )";
        if [ "$line" == "" ]; then continue; fi
        local columns=( $line );
        local id="${columns[0]}";
        local names="${columns[1]}";
        local image="${columns[2]}";
        _cli_message "- \033[91mremove\033[0m container $names ($id) ---> has image $image";
        docker stop "$id" && docker rm "$id" 2> $VERBOSE;
    done <<< "$( docker ps -aq --format '{{.ID}}\t{{.Names}}\t{{.Image}}' )";
}

function docker_remove_all_images() {
    local line;
    while read line; do
        line="$( _trim "$line" )";
        if [ "$line" == "" ]; then continue; fi
        local columns=( $line );
        local id="${columns[0]}";
        local image="${columns[1]}";
        local tag="${columns[2]}";
        _cli_message "- \033[91mremove\033[0m image $image:$tag ($id)";
        docker rmi -f "$id" 2> $VERBOSE;
    done <<< "$( docker images -aq --format '{{.ID}}\t{{.Repository}}\t{{.Tag}}' )";
}

##############################################################################
# AUXILIARY METHODS: DOCKER/WHALES STATE
##############################################################################

function get_whales_state_of_docker() {
    local state="out";
    [[ -f "$WHALES_FILE_DOCKER_STATE" ]] && state="$( head -n 1 "$WHALES_FILE_DOCKER_STATE" )";
    ! ( echo "$state" | grep -Eq "^(in|out)$" ) && state="out";
    echo $state;
}

function is_docker() {
    local state=$( get_whales_state_of_docker );
    [[ "$state" == "in" ]] && return 0 || return 1;
}

function get_whales_state_of_whales() {
    local state=0;
    [[ -f "$WHALES_FILE_WHALES_STATE" ]] && state="$( head -n 1 "$WHALES_FILE_WHALES_STATE" )";
    ! ( echo "$state" | grep -Eq "^(on|off)$" ) && state="off";
    echo $state;
}

function is_whales_active() {
    local state=$( get_whales_state_of_whales );
    [[ "$state" == "on" ]] && return 0 || return 1;
}

##############################################################################
# MAIN METHODS:
##############################################################################

function whales_activate() { echo "on" >| $WHALES_FILE_WHALES_STATE; }

function whales_deactivate() { echo "off" >| $WHALES_FILE_WHALES_STATE; }

function whales_set_ports() {
    local arguments=( "$@" );
    local ports;
    local port;
    for port in "${arguments[@]}"; do
        port="$( echo "$port" | sed -E "s/[[:space:]]//g" )";
        [ "$port" == "" ] && continue || [ "$ports" == "" ] && ports="-p $port" || ports="$ports -p $port";
    done
    export WHALES_PORTS_OPTIONS="$ports";
}

function whales_add_port() {
    local port="$( echo "$1" | sed -E "s/[[:space:]]//g" )";
    local ports="$WHALES_PORTS_OPTIONS";
    [ "$ports" == "" ] && ports="-p $port" || ports="$ports -p $port";
    export WHALES_PORTS_OPTIONS="$ports";
}

function select_service() {
    local service="$1";
    local success=true;
    export WHALES_DOCKER_SERVICE="$service";
    docker_set_service_image     "$service" || success=false;
    docker_set_service_container "$service" || success=false;
    ( $success ) && return 0 || return 1;
}

function get_docker_service() {
    local project="$WHALES_PROJECT_NAME";
    local service="$1";
    local force_build=$2;
    [ "$force_build" == "" ] && force_build=false;
    local success;

    # Attempt to set service
    select_service "$service" 2> $VERBOSE && return;
    ! ( $force_build ) && _log_error "Could not set the service to \033[1m$service\033[0m." && return 1;

    # Force start docker servic, if not already up:
    _log_info "FORCE-BUILD DOCKER SERVICE.";
    run_docker_compose_build "$project" "$service";
    run_docker_compose "$project" up "$service";

    # Attempt to set service again:
    success=false;
    select_service "$service" 2> $VERBOSE && success=true;
    ! ( $success ) && _log_error "Could not set the service to \033[1m$service\033[0m." && return 1;

    # Rename container to Whales scheme (see .env in setup folder):
    local container_id="${WHALES_DOCKER_CONTAINER_ID}";
    local container_name="$( docker_create_unused_container_name_for_service "$service" )";
    _log_info "RENAME CONTAINER \033[1m$container_id\033[0m ---> \033[92;1m$container_name\033[0m.";
    docker rename "$container_id" "$container_name";
}
