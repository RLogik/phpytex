#!/bin/bash

##############################################################################
#    DESCRIPTION: Library of common utility functions.
#    Include using source .whales/.lib.utils.sh
##############################################################################

##############################################################################
# FOR OS SENSITIVE COMMANDS
##############################################################################

function is_linux() {
    [ "$OSTYPE" == "msys" ] && return 1 || return 0;
}

function dos_to_unix() {
    ( dos2unix --version 2> $VERBOSE >> $VERBOSE ) && dos2unix -q $1 && return;
    _log_fail "Install \033[1mdos2unix\033[0m for your system and ensure the command can be called in bash before proceeding. Cf. https://command-not-found.com/dos2unix, https://chocolatey.org/packages/dos2unix, etc.";
}

function clean_scripts_dos2unix() {
    local setup_path="$1";
    local path;
    while read path; do
        [ "$path" == "" ] && continue;
        dos_to_unix "$path";
    done <<< "$( ls -a {,$setup_path/}{,.}*.sh 2> $VERBOSE )";
}

function check_jq_exists() {
    ( jq --version 2> $VERBOSE >> $VERBOSE ) && return 0 || return 1;
}

##############################################################################
# AUXILIARY METHODS: READING CLI ARGUMENTS
##############################################################################

function has_arg() {
    echo "$1" | grep -Eq "(^.*[[:space:]]|^)$2([[:space:]].*$|$)" && return 0 || return 1;
}

function get_kwarg() {
    local value="$(echo "$1" | grep -Eq "(^.*\s|^)$2=" && echo "$1" | sed -E "s/(^.*[[:space:]]|^)$2=(\"([^\"]*)\"|\'([^\']*)\'|([^[:space:]]*)).*$/\3\4\5/g" || echo "")";
    echo $value | grep -Eq "[^[:space:]]" && echo "$value" || echo "$3";
}

function get_all_kwargs() {
    local arguments="$1";
    local key="$2";
    local get_one=$3;
    local default="$4"; # only used if $get_one == true
    local pattern="(^.*[[:space:]]|^)$key(\"([^\"]*)\"|\'([^\']*)\'|([^[:space:]]*)).*$";
    while ! [[ "$arguments" == "" ]]; do
        if ! ( echo "$arguments" | grep -Eq "$pattern" ); then
            arguments="";
            break;
        fi
        local value="$(echo "$arguments" | sed -E "s/$pattern/\3\4\5/g" || echo "")";
        arguments="$(echo "$arguments" | sed -E "s/$pattern/\1/g" || echo "")";
        echo "$value";
        ( $get_one ) && return 0;
    done
    ( $get_one ) && echo "$default";
}

function get_one_kwarg() {
    get_all_kwargs "$1" "$2" true "$3";
}

function get_one_kwarg_space() {
    local value="$( get_all_kwargs "$1" "$2[[:space:]]+" true "$3" )";
    ( echo "$value" | grep -Eq "^-+" ) && value="$3";
    echo "$value";
}

##############################################################################
# AUXILIARY METHODS: LOGGING AND CLI-INPUTS
##############################################################################

function check_answer() {
    echo "$1" | grep -q -E -i "^(y|yes|j|ja|1)$";
}

function _cli_ask() {
    echo -ne "$1" >> $OUT;
}

export CLI_ANSWER="";
function _cli_ask_expected_answer() {
    local msg="$1";
    local answerpattern="$2";
    local read_break_char;
    local symb;
    CLI_ANSWER="";
    while ( true ); do
        echo -ne "$msg" >> $OUT;
        ## read in CLI_ANSWER character by character:
        CLI_ANSWER="";
        read_break_char=false;
        while IFS= read -rN 1 symb; do
            case "$symb" in
                $'\04') read_break_char=true          ;&
                $'\n')  break                         ;;
                *)      CLI_ANSWER="$CLI_ANSWER$symb" ;;
            esac
        done
        ( $read_break_char ) && echo -e "" >> $OUT && exit 1;
        ( echo "$CLI_ANSWER" | grep -Eq "$2" ) && break;
    done
}

function _cli_ask_expected_answer_secure() {
    local msg="$1";
    local answerpattern="$2";
    local mask="$3";
    local read_break_char;
    local symb;
    CLI_ANSWER="";
    while ( true ); do
        echo -ne "$msg" >> $OUT;
        stty -echo;
        ## read in CLI_ANSWER character by character:
        CLI_ANSWER="";
        read_break_char=false;
        while IFS= read -rN 1 symb; do
            case "$symb" in
                $'\04') read_break_char=true          ;&
                $'\n')  break                         ;;
                *)      CLI_ANSWER="$CLI_ANSWER$symb" ;;
            esac
        done
        stty echo;
        ( $read_break_char ) && echo -e "" >> $OUT && exit 1;
        [[ "$mask" == "true" ]] && echo -e "$( echo $CLI_ANSWER | sed -r 's/./\*/g' )" || echo -e "$mask";
        ( echo "$CLI_ANSWER" | grep -Eq "$2" ) && break;
    done
}

function _cli_trailing_message() {
    echo -ne "$1" >> $OUT;
}

function _cli_message() {
    if [ "$2" == "true" ]; then
        _cli_trailing_message "$1";
    else
        echo -e "$1" >> $OUT;
    fi
}

function _log_info() {
    _cli_message "${LOGGINGPREFIX}[\033[94;1mINFO\033[0m] $1" $2;
}

function _log_debug() {
    _cli_message "${LOGGINGPREFIX}[\033[95;1mDEBUG\033[0m] $1" $2;
    if ! [ -f "$PATH_LOGS/$FILENAME_LOGS_DEBUG" ]; then
        mkdir "$PATH_LOGS" 2> $VERBOSE;
        touch "$PATH_LOGS/$FILENAME_LOGS_DEBUG";
    fi
    echo "$1" >> "$PATH_LOGS/$FILENAME_LOGS_DEBUG";
}

function _log_warn() {
    _cli_message "${LOGGINGPREFIX}[\033[93;1mWARNING\033[0m] $1" $2;
}

function _log_error() {
    if [ "$2" == "true" ]; then
        echo -ne "${LOGGINGPREFIX}[\033[91;1mERROR\033[0m] $1" >> $ERR;
    else
        echo -e "${LOGGINGPREFIX}[\033[91;1mERROR\033[0m] $1" >> $ERR;
    fi
}

function _log_fail() {
    _log_error "$1" $2;
    exit 1;
}

##############################################################################
# AUXILIARY METHODS: HELP
##############################################################################

function _help_cli_key_values() {
    local arguments=( "$@" );
    local key="${arguments[0]}";
    local indent="${arguments[1]}";
    local values="";
    for arg in "${arguments[@]:2}"; do
        if ! [ "$values" == "" ]; then values="$values|"; fi
        values="$values\033[92;1m$arg\033[0m";
    done
    local cmd="\033[93;1m$key\033[0m$indent$values";
    echo "$cmd";
}

function _help_cli_key_description() {
    local arguments=( "$@" );
    local key="${arguments[0]}";
    local indent="${arguments[1]}";
    local descr="${arguments[@]:2}";
    local cmd="\033[93;1m$key\033[0m$indent\033[2;3m$descr\033[0m";
    echo "$cmd";
}

function _help_cli_values() {
    local arguments=( "$@" );
    local cmd="";
    for arg in "${arguments[@]}"; do
        ! [ "$cmd" == "" ] && cmd="$cmd|";
        cmd="$cmd\033[92;1m$arg\033[0m";
    done
    echo "$cmd";
}

##############################################################################
# AUXILIARY METHODS: PROGRESSBAR
##############################################################################

function show_progressbar() {
    local pid=$1 # Process Id of the previous running command

    function shutdown() {
        tput cnorm; # reset cursor
    }

    function cursorBack() {
        echo -en "\033[$1D";
    }

    trap shutdown EXIT;

    local displayed=false;
    # tput civis; # cursor invisible
    while kill -0 $pid 2> $VERBOSE; do
        if [ "$displayed" == "false" ]; then
            _log_info "pending... $PENDING_SYMBOL" "true";
            displayed=true;
        else
            _cli_trailing_message "$PENDING_SYMBOL";
        fi
        sleep $WAIT_PERIOD_IN_SECONDS;
    done
    # tput cnorm; # cursor visible
    wait $pid;
    local success=$?;
    [ "$displayed" == "true" ] && _cli_trailing_message "\n";
    return $success;
}

##############################################################################
# AUXILIARY METHODS: STRINGS
##############################################################################

function _trim() {
    _trim_trailing_spaces "$( _trim_leading_spaces "$1" )";
}

function _trim_leading_spaces() {
    echo "$1" | sed -E "s/^[[:space:]]+(.*)$/\1/g"
}

function _trim_trailing_spaces() {
    echo "$1" | sed -E "s/(^.*[^[:space:]]+|^)[[:space:]]+$/\1/g"
}

function to_lower() {
    echo "$(echo "$1" |tr '[:upper:]' '[:lower:]')";
}

function to_upper() {
    echo "$(echo "$1" |tr '[:lower:]' '[:upper:]')";
}

function is_comment() {
    echo "$1" | grep -Eq "^\s*\#" && return 0 || return 1;
}

function _trim_trailing_comments() {
    echo "$1" | sed -E "s/(^[^\#]*)\#.*$/\1/g" | sed -E "s/(^.*[^[:space:]]+|^)[[:space:]]+$/\1/g";
}

## Replaces all occurrences of ~ with $HOME.
## NOTE: use / to replace first, // to replace all.
function expand_path() {
    echo "${1//\~/$HOME}";
}

##############################################################################
# AUXILIARY METHODS: JSON
##############################################################################

function json_dictionary_kwargs_jq() {
    ! ( check_jq_exists ) && _log_fail "You need to install \033[1mjq\033[0m to use this method.";
    local json="$1";
    local format=".key + \" \" + (.value|tostring)";
    echo "$json" |  jq -r "to_entries | map($format) | .[]";
}

# Only for json dictionaries of type Dict[str,(str|number|bool)],
function json_dictionary_kwargs() {
    local json="$1";
    # Remove outer braces:
    json="$( echo "$json" | sed -E "s/^\{|\}$//g" )";
    # Recursively extract keys and values from right-to-left:
    local keypattern="[a-zA-Z0-9\.-_]";
    local pattern="((^.*),|(^))\"($keypattern*)\":(\"(.*)\"|(.*))$";
    function json_dictionary_kwargs_recursive() {
        local json="$1";
        [ "$json" == "" ] && return;
        ! ( echo "$json" | grep -Eq "$pattern" ) && return;
        local key="$(   echo "$json" | sed -E "s/$pattern/\4/g"   )";
        local value="$( echo "$json" | sed -E "s/$pattern/\6\7/g"   )";
        json="$(        echo "$json" | sed -E "s/$pattern/\2\3/g" )";
        json_dictionary_kwargs_recursive "$json";
        echo "$key $value";
    }
    json_dictionary_kwargs_recursive "$json";
}

##############################################################################
# AUXILIARY METHODS: YAML CONFIG FILES
##############################################################################

function has_config_key() {
    local config="$1";
    local key="$2";
    ! [ -f $file ] && _log_fail "Config file \033[1m$config\033[0m not found!";
    echo "( cat $config )" | grep -Eq  "^\s*$key:" && return 0 || return 1;
}

function json_parse() {
    local args=( "$@" );
    ! ( jq --version 2> $VERBOSE >> $VERBOSE ) && _log_fail "Install \033[1mjq\033[0m for your system and ensure the command can be called in bash before proceeding. Cf. https://command-not-found.com/jq, https://chocolatey.org/packages/jq, etc.";
    echo "${args[0]}" | jq ${args[@]:1};
}

function yaml_parse() {
    local args=( "$@" );
    ! ( yq --version 2> $VERBOSE >> $VERBOSE ) && _log_fail "Install \033[1myq\033[0m for your system and ensure the command can be called in bash before proceeding. Cf. https://command-not-found.com/yq, https://chocolatey.org/packages/yq, etc.";
    local lines="$( yq eval --tojson "${args[0]}" )";
    json_parse "$lines" ${args[@]:1};
}

function get_config_key_value_simpleversion() {
    local config="$1";
    local key="$2";
    local default="$3";
    ! [ -f $config ] && _log_fail "Config file \033[1m$config\033[0m not found!";
    ## use sed -n .... /p to delete all non-matching lines
    ## store matches in an array
    local lines=( $(echo "( cat $config )" | sed -n -E "s/^[[:space:]]*$key:(.*)$/\1/p") );
    ## extract the 0th entry, if it exists, otherwise return default.
    echo "$([ ${#lines[@]} -gt 0 ] && echo "$(_trim "${lines[0]}")" || echo "$default")";
}

function get_config_key_value() {
    local config="$1";
    local key="$2";
    local default="$3";
    ! [ -f $config ] && _log_fail "Config file \033[1m$config\033[0m not found!";
    local value="$( yaml_parse "$config" --raw-output ".$key" 2> $VERBOSE || echo "$default" )";
    [ "$value" == "null" ] && value="$default";
    echo "$value";
}

function get_config_boolean() {
    local config="$1";
    local key="$2";
    local default="$3";
    local value="$( get_config_key_value "$config" "$key" "$default" )";
    [ "$value" == "true" ] && return 0 || return 1;
}

##############################################################################
# AUXILIARY METHODS: FILES AND FOLDERS
##############################################################################

function copy_file() {
    local args="$@"
    local file="$(                  get_kwarg "$args" "file" ""   )";
    local folder_from_formatted="$( get_kwarg "$args" "from" ""   )";
    local folder_to_formatted="$(   get_kwarg "$args" "to" ""     )";
    local rename="$(                get_kwarg "$args" "rename" "" )";

    local folder_from="$( expand_path "$folder_from_formatted" )";
    local folder_to="$(   expand_path "$folder_to_formatted"   )";

    if ! [ -d "$folder_from" ]; then
        _log_error "For copy-file command: source folder \033[1m$folder_from_formatted\033[0m does not exist!";
        return;
    fi
    if ! [ -d "$folder_to" ]; then
        _log_error "For copy-file command: destination folder \033[1m$folder_to_formatted\033[0m does not exist!";
        return;
    fi
    if ! [ -f "$folder_from/$file" ]; then
        _log_error "For copy-file command: file \033[1m$folder_from_formatted/$file\033[0m could not be found!";
        return;
    fi

    [ "$rename" == "" ] && rename="$file";

    cp "$folder_from/$file" "$folder_to/$rename" && _log_info "Copied \033[1m$folder_from_formatted/$file\033[0m to \033[1m$folder_to_formatted/$rename\033[0m." || _log_fail "Copy-file command failed.";
}

function copy_dir() {
    local args="$@"
    local dir="$(                   get_kwarg "$args" "dir" ""  )";
    local folder_from_formatted="$( get_kwarg "$args" "from" "" )";
    local folder_to_formatted="$(   get_kwarg "$args" "to" ""   )";

    local folder_from="$( expand_path "$folder_from_formatted" )";
    local folder_to="$(   expand_path "$folder_to_formatted"   )";

    if ! [ -d "$folder_from" ]; then
        _log_error "For copy-dir command: source folder \033[1m$folder_from_formatted\033[0m does not exist!";
        return;
    fi
    if ! [ -d "$folder_to" ]; then
        _log_error "For copy-dir command: destination folder \033[1m$folder_to_formatted\033[0m does not exist!";
        return;
    fi
    if ! [ -d "$folder_from/$dir" ]; then
        _log_error "For copy-dir command: directory \033[1m$folder_from_formatted/$dir\033[0m could not be found!";
        return;
    fi

    cp -r "$folder_from/$dir" "$folder_to" && _log_info "Copied \033[1m$folder_from_formatted/$dir\033[0m to \033[1m$folder_to_formatted/$rename\033[0m." || _log_fail "Copy-dir command failed.";
}

function remove_file() {
    local fname="$1";
    [ -f "$fname" ] && rm -f "$fname" && _log_info "Removed file \033[1m$fname.\033[0m" || _log_info "Nothing to remove: the file \033[1m$fname\033[0m does not exist.";
}

function remove_dir() {
    local path="$1";
    [ -f "$path" ] && rm -r "$path" && _log_info "Removed directory \033[1m$path.\033[0m" || _log_info "Nothing to remove: the directory \033[1m$path\033[0m does not exist.";
}

function remove_dir_force() {
    local path="$1";
    [ -f "$path" ] && rm -rf "$path" && _log_info "Removed directory \033[1m$path.\033[0m" || _log_info "Nothing to remove: the directory \033[1m$path\033[0m does not exist.";
}

##############################################################################
# AUXILIARY METHODS: CLEANING
##############################################################################

function clean_by_pattern() {
    local path="$1";
    local pattern="$2"
    local force=$3;
    ! ( ls $path | grep -q -E "$pattern" ) && return;
    _log_info "Files to be removed:";
    ls $path | grep -E "$pattern" | awk -v PATH=$path '{print "    \033[94m" PATH "/" $1 "\033[0m"}' >> $OUT;
    if ! ( $force ); then
        _cli_ask_expected_answer "    Do you wish to proceed? (y/n) " "^(y|n)$";
        ! [[ "$CLI_ANSWER" == "y" ]] && _log_info "skipped." && return;
    fi
    ls $path | grep -E "$pattern" | awk -v PATH=$path '{print PATH "/" $1}' | xargs rm -r;
    _log_info "deleted.";
}

function clean_folder_contents() {
    local folder="$1";
    local path;
    while read path; do
        [ "$path" == "" ] && continue;
        [ -f "$path" ] && remove_file "$path" >> $VERBOSE && continue;
        [ -d "$path" ] && rm -rf "$path" && continue;
    done <<< $( find "$folder" -mindepth 1 2> $VERBOSE );
    _log_info "(\033[91mforce removed\033[0m) contents of \033[94m$folder/\033[0m";
}

function clean_all_folders_of_pattern() {
    local pattern="$1";
    local objects=( $( find * -type d -name ${pattern} ) );
    local n=${#objects[@]};
    [[ $n -gt 0 ]] && find * -type d -name ${pattern} | awk '{print $1}' | xargs rm -rf;
    _log_info "    (\033[91mforce removed\033[0m) $n x \033[94m${pattern}\033[0m folders";
}

function clean_all_files_of_pattern() {
    local pattern="$1";
    local objects=( $( find * -type f -name ${pattern} ) );
    local n=${#objects[@]};
    [[ $n -gt 0 ]] && find * -type f -name ${pattern} | awk '{print $1}' | xargs rm -rf;
    _log_info "    (\033[91mforce removed\033[0m) $n x \033[94m${pattern}\033[0m files";
}
