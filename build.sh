#! /bin/bash

##############################################################################
# FILE: (bash script) build
# AUTHOR: R-Logik, Deutschland. https://github.com/RLogik/phpytex
# CREATED: 28.07.2020
# DESCRIPTION:
#   script for building the phpytex project.
# NOTES:
#
#    Installation:
#    ~~~~~~~~~~~~~
#    1. Go to https://github.com/RLogik/bash-scripts/blob/master/python-projects
#      and download the bash scripts:
#         python_for_pyinstaller
#         compile_pyinstaller
#      for your system.
#      !! You need to install a suitable version of Python
#        in order for these work! (See these files for more.)
#    2. modify the first 2 lines of this script if necessary.
#    3. you may need to run
#          dos2unix <name of this script>
#       beforehand. Then run
#          [sudo] chmod +x <name of this script>
#       in bash, to be able to use this script.
#
#    Usage:
#    ~~~~~~~~~~~~~
#
#       ./build.sh [skip-build] [--release]
#
#    This compiles the project via compile_pyinstaller,
#    which first creates a python virtualenvironment in ./env,
#    installs the requirements, then runs PyInstaller over the setup.py file.
#
#    The arguments are as follows:
#
#       skip-build ⟹ the PyInstall process will be skipped
#       --release  ⟹ the created binary will be zipped and version for the release.
#
#    Note: There are safety measures in place to prevent willy-nilly overwriting
#    of existing release versions.
#
##############################################################################

SCRIPTARGS="$@";

. .lib.sh;

app_name="phpytex";
python_path="$(python_for_pyinstaller --which)";
spec_path="src";

if ! [ $(has_arg "$SCRIPTARGS" "skip-build") ]; then
    # NOTE for each --add-data argument the first parts (in 1:2) are relative to spec_path.
    compile_pyinstaller \
        python-path="$python_path" \
        app-name="$app_name" \
        setup-file=setup.py \
        spec-path="$spec_path" \
        --add-data "config.yml:src" \
        --add-data "./../dist/VERSION:src" \;
fi

if [ $(has_arg "$SCRIPTARGS" "-*release") ]; then
    post_build_create_release_version
fi
