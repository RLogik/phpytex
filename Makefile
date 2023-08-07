SHELL:=/usr/bin/env bash
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Makefile
# NOTE: Do not change the contents of this file!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

include .env

################################
# VARIABLES
################################

ARTEFACT_NAME:=${APPNAME}
PYTHON:=python3
ifeq ($(OS),Windows_NT)
ARTEFACT_NAME:=${APPNAME}.exe
PYTHON=py -3
endif

################################
# Macros
################################

define create_file_if_not_exists
	@touch "$(1)";
endef

define create_folder_if_not_exists
	if ! [ -d "$(1)" ]; then mkdir "$(1)"; fi
endef

define delete_if_file_exists
	@if [ -f "$(1)" ]; then rm "$(1)"; fi
endef

define delete_if_folder_exists
	@if [ -d "$(1)" ]; then rm -rf "$(1)"; fi
endef

define clean_all_files
	@find . -type f -name "$(1)" -exec basename {} \;
	@find . -type f -name "$(1)" -exec rm {} \; 2> /dev/null
endef

define clean_all_folders
	@find . -type d -name "$(1)" -exec basename {} \;
	@find . -type d -name "$(1)" -exec rm -rf {} \; 2> /dev/null
endef

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

################################
# BASIC TARGETS: setup, build, run
################################
setup: check-system-requirements setup-no-checks
setup-no-checks:
	@${PYTHON} -m pip install -r "requirements"
build:
	@source scripts/.lib.sh && run_create_artefact
run:
	@${PYTHON} src/main.py;

dev:
	@make build
	@cp dist/phpytex ${HOME}/.phpytex/dev

################################
# TARGETS: testing
################################
tests: unit-tests integration-tests
tests-inspect: unit-tests integration-tests-inspect
unit-tests:
	@# For logging purposes (since stdout can be rechanneled):
	@$(call delete_if_file_exists,logs/debug.log)
	@$(call create_folder_if_not_exists,logs)
	@$(call create_file_if_not_exists,logs/debug.log)
	@# for python unit tests:
	@${PYTHON} -m pytest --cache-clear --verbose -k test_
	@cat logs/debug.log
integration-tests:
	@${PYTHON} tests/cases.py
integration-tests-inspect:
	@${PYTHON} tests/cases.py --options "inspect"
################################
# TARGETS: examples/demos
################################
examples:
	source scripts/.lib.sh && run_create_examples
################################
# AUXILIARY (INTERNAL TARGETS)
################################
check-system-requirements:
	@if ! ( ${PYTHON} --version >> /dev/null 2> /dev/null ); then \
		echo "Install Python 3.10.x first!"; \
		exit 1; \
	fi
	@${PYTHON} --version
################################
# TARGETS: clean
################################
clean:
	@echo "All system artefacts will be forcibly removed."
	@$(call clean_all_files,.DS_Store)
	@echo "All test + build artefacts will be forcibly removed."
	@$(call delete_if_folder_exists,logs)
	@$(call delete_if_file_exists,dist/${ARTEFACT_NAME})
	@$(call clean_all_folders,__pycache__)
	@$(call clean_all_folders,.pytest_cache)
	@exit 0
