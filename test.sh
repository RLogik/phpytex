#!/bin/bash

##############################################################################
# FILE: (bash script) test
# AUTHOR: R-Logik, Deutschland. https://github.com/RLogik/phpytex
# CREATED: 28.07.2020
# DESCRIPTION:
#   script for testing the phpytex project.
# NOTES:
#
#     Installation:
#     ~~~~~~~~~~~~~
#     1. modify the first 2 lines of this script if necessary.
#     2. you may need to run
#            dos2unix <name of this script>
#        beforehand. Then run
#            [sudo] chmod +x <name of this script>
#        in bash, to be able to use this script.
#
#     Usage:
#     ~~~~~~~~~~~~~
#
#       ./test.sh
#
##############################################################################

SCRIPTARGS="$@";

. .lib.sh;

echo -e "The current version being tested is \033[1;92m$(get_version)\033[0m...";
run_tests $SCRIPTARGS
