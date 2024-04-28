#!/usr/bin/env bash

source .env

dist="$( dirname $( dirname "${0}" ) )/${VERSION}"

jf="${dist}/justfile"

if [[ ${#@} == 1 ]] && [[ "$1" == "run" ]]; then
    just --justfile "${jf}" run-cli  "run" "TRANSPILE" --path "${PWD}"
else
    just --justfile "${jf}" run-cli  "$@"
fi
