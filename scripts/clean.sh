#!/usr/bin/env bash

##############################################################################
#    DESCRIPTION: Script for cleaning-processes.
#
#    Usage:
#    ~~~~~~
#    ./clean.sh [options]
##############################################################################

SCRIPTARGS="$@";
FLAGS=( $@ );
ME="scripts/clean.sh";

source scripts/.lib.sh;

run_clean_artefacts;

exit 0;
