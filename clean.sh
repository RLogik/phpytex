#! /bin/bash

##############################################################################
# FILE: (bash script) build
# AUTHOR: R-Logik, Deutschland. https://github.com/RLogik/phpytex
# CREATED: 28.07.2020
# DESCRIPTION:
#   script for cleaning the phpytex project of build artefacts
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
#       ./clean.sh [--f, --force] [--q, --quiet]
#
#    This cleans the project of the folders and a few files,
#    created by the build process, except for the release.
#    The arguments are as follows:
#
#       --force ⟹ All standard files will be deleted without confirmation.
#       --quiet ⟹ No console output (only with force mode).
#
##############################################################################

SCRIPTARGS="$@";

. .lib.sh;

################################################################
# AUXILLIARY FUNCTIONS:
################################################################
function exists_by_pattern() {
    path="$1";
    pattern="$2"
    ls $path | grep -q -E "$pattern" && echo 1 || echo 0;
}

function clean_by_pattern() {
    path="$1";
    pattern="$2"

    if [[ $(exists_by_pattern "$path" "$pattern") == 1 ]]; then
        if [[ $force ]]; then
            ls $path | grep -E "$pattern" | awk -v PATH=$path '{print "    \033[94m" PATH "/" $1 "\033[0m"}' >> $OUTPUT;
            ls $path | grep -E "$pattern" | awk -v PATH=$path '{print PATH "/" $1}' | xargs rm -r;
        else
            echo -e "- \033[91mRemoving\033[0m:";
            ls $path | grep -E "$pattern" | awk -v PATH=$path '{print "    \033[94m" PATH "/" $1 "\033[0m"}';
            echo -e -n "  Do you wish to proceed? (y/n) "
            read answer;
            if ( check_answer "$answer" ); then
                echo -e "  Deleting...";
                ls $path | grep -E "$pattern" | awk -v PATH=$path '{print PATH "/" $1}' | xargs rm -r;
            else
                echo -e "  Skipping.";
            fi
            echo -e "";
        fi
    fi
}
################################################################

force=$(has_arg "$SCRIPTARGS" "-+(f|force)");
quiet=$(has_arg "$SCRIPTARGS" "-+(q|quiet)");
OUTPUT="$( [[ $force && $quiet ]] && echo "$VERBOSE" || echo "$OUT" )";

echo -e "" >> $OUTPUT;
echo -e "\033[1;4;32mGarbage collection:\033[0m" >> $OUTPUT;

clean_by_pattern . "^env$";
clean_by_pattern . "^build$";
clean_by_pattern . "^logs$";
clean_by_pattern . "^.*.egg.info$";
clean_by_pattern . "^.*.spec$";
clean_by_pattern dist "^.*.egg$";
clean_by_pattern dist "^.*_entry.py$";
clean_by_pattern dist "^__pycache__$";

echo -e "\033[1;32mFinished!\033[0m" >> $OUTPUT;
echo -e "" >> $OUTPUT;
