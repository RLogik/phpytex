# set shell := [ "bash", "-c" ]
_default:
    @- just --unsorted --list
menu:
    @- just --unsorted --choose
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Justfile
# Recipes for various workflows.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

set dotenv-load := true
set positional-arguments := true

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_ROOT := justfile_directory()
CURRENT_DIR := invocation_directory()
OS := if os_family() == "windows" { "windows" } else { "linux" }
PYVENV := if os_family() == "windows" { "python" } else { "python3" }
PYVENV_ON := if os_family() == "windows" { ". .venv/Scripts/activate" } else { ". .venv/bin/activate" }
LINTING := "black"
GITHOOK_PRECOMMIT := "pre_commit"
GEN_MODELS := "datamodel_code_generator"
GEN_APIS := "openapi-generator"
TOOL_TEST_BDD := "behave"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Macros
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_create-file-if-not-exists fname:
    #!/usr/bin/env bash
    touch "{{fname}}";
    exit 0;

_create-folder-if-not-exists path:
    #!/usr/bin/env bash
    if ! [[ -d "{{path}}" ]]; then
        mkdir -p "{{path}}";
    fi
    exit 0;

_create-temp-folder path="." name="tmp":
    #!/usr/bin/env bash
    k=-1;
    tmp_folder="{{path}}/{{name}}";
    while [[ -d "${tmp_folder}" ]] || [[ -f "${tmp_folder}" ]]; do
        k=$(( $k + 1 ));
        tmp_folder="{{path}}/{{name}}_${k}";
    done
    mkdir "${tmp_folder}";
    echo "${tmp_folder}";
    exit 0;

_delete-if-file-exists fname:
    #!/usr/bin/env bash
    if [[ -f "{{fname}}" ]]; then
        rm "{{fname}}";
    fi
    exit 0;

_delete-if-folder-exists path:
    #!/usr/bin/env bash
    if [[ -d "{{path}}" ]]; then
        rm -rf "{{path}}";
    fi
    exit 0;

_clean-all-files path pattern:
    #!/usr/bin/env bash
    find {{path}} -type f -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    find {{path}} -type f -name "{{pattern}}" -exec rm {} \; 2> /dev/null
    exit 0;

_clean-all-folders path pattern:
    #!/usr/bin/env bash
    find {{path}} -type d -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    find {{path}} -type d -name "{{pattern}}" -exec rm -rf {} \; 2> /dev/null
    exit 0;

_check-python-tool tool name:
    @just _check-tool "{{PYVENV}} -m {{tool}}" "{{name}}"

_check-python-bin tool name:
    @just _check-tool "{{tool}}" "{{name}}"

_check-tool tool name:
    #!/usr/bin/env bash
    success=false
    {{PYVENV_ON}} && {{tool}} --version >> /dev/null 2> /dev/null && success=true;
    {{PYVENV_ON}} && {{tool}} --help >> /dev/null 2> /dev/null && success=true;
    # NOTE: if exitcode is 251 (= help or print version), then render success.
    if [[ "$?" == "251" ]]; then success=true; fi
    # FAIL tool not installed
    if ( $success ); then
        echo -e "Tool \x1b[2;3m{{name}}\x1b[0m installed correctly.";
        exit 0;
    else
        echo -e "Tool \x1b[2;3m{{name}}\x1b[0m did not work." >> /dev/stderr;
        echo -e "Ensure that \x1b[2;3m{{name}}\x1b[0m (-> \x1b[1mjust build\x1b[0m) installed correctly and system paths are set." >> /dev/stderr;
        exit 1;
    fi

_generate-documentation path_schema target_path name:
    @{{PYVENV_ON}} && {{GEN_APIS}} generate \
        --skip-validate-spec \
        --input-spec {{path_schema}}/schema-{{name}}.yaml \
        --generator-name markdown \
        --output "{{target_path}}/{{name}}"

_generate-documentation-recursively path_schema target_path:
    #!/usr/bin/env bash
    # skip if no files exist
    ls -f {{path_schema}}/schema-*.yaml >> /dev/null 2> /dev/null || exit 0;
    # otherwise proceed
    while read path; do
        if [[ "${path}" == "" ]]; then continue; fi
        path="${path##*/}";
        name="$( echo """${path}""" | sed -E """s/^schema-(.*)\.yaml$/\1/g""")";
        echo "- generate documentation for ${name}."
        just _generate-documentation "{{path_schema}}" "{{target_path}}" "${name}";
    done <<< "$( ls -f {{path_schema}}/schema-*.yaml )";
    exit 0;

_generate-models path_schema target_path name:
    @{{PYVENV_ON}} && {{PYVENV}} -m {{GEN_MODELS}} \
        --input-file-type openapi \
        --output-model-type pydantic_v2.BaseModel \
        --encoding "UTF-8" \
        --disable-timestamp \
        --use-schema-description \
        --field-constraints \
        --capitalise-enum-members \
        --enum-field-as-literal one \
        --set-default-enum-member \
        --use-subclass-enum \
        --allow-population-by-field-name \
        --snake-case-field \
        --strict-nullable \
        --target-python-version 3.11 \
        --input {{path_schema}}/schema-{{name}}.yaml \
        --output {{target_path}}/{{name}}.py

_generate-models-recursively path_schema target_path:
    #!/usr/bin/env bash
    # skip if no files exist
    ls -f {{path_schema}}/schema-*.yaml >> /dev/null 2> /dev/null || exit 0;
    # otherwise proceed
    while read path; do
        if [[ "${path}" == "" ]]; then continue; fi
        path="${path##*/}";
        name="$( echo """${path}""" | sed -E """s/^schema-(.*)\.yaml$/\1/g""")";
        echo "- generate models for ${name}."
        just _generate-models "{{path_schema}}" "{{target_path}}" "${name}";
    done <<< "$( ls -f {{path_schema}}/schema-*.yaml )";
    exit 0;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: githooks
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# NOTE: this is necessary, as pre-commit does not properly run multiline commands

githook-lint *args:
    @just lint-check "$0" # perform linting without changes
    @# just lint "$0" # perform linting with changes
    @# git add "$0" # add to commit

githook-utests *args:
    @just test-unit "$0"

githook-btests *args:
    #!/usr/bin/env bash
    # just run-api &        # run the api
    # export PID=$!         # store process id of api
    # just test-behave "$0" # run the test
    # kill $PID             # terminate the api
    echo "behavioural tests skipped - please run manually!";

githook-qa *args:
    #!/usr/bin/env bash
    just build-skip-requirements
    just prettify
    just tests-unit
    # just run-api &    # run the api
    # export PID=$!     # store process id of api
    # just tests-behave # run the test
    # kill $PID         # terminate the api
    echo "behavioural tests skipped - please run manually!";

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: build
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

setup:
    @echo "TASK: SETUP"
    @- cp -n "templates/template.env" ".env"

build:
    @echo "TASK: BUILD"
    @just build-venv
    @just build-requirements
    @just check-system-requirements
    @just build-models
    @just build-githook-pc

build-skip-requirements:
    @echo "TASK: BUILD (skip installing requirements)"
    @just build-venv
    @just check-system-requirements
    @just build-models

build-deployment:
    @echo "TASK: BUILD FOR DEPLOYMENT"
    @just build-venv
    @just build-requirements

build-venv:
    @- ${PYTHON_PATH} -m venv .venv

# cf. https://pre-commit.com
build-githook-pc:
    #!/usr/bin/env bash
    echo "SUBTASK: build githook"
    if [[ -d ".git" ]]; then
        git config --unset-all core.hooksPath
        {{PYVENV_ON}} && {{PYVENV}} -m pre_commit uninstall
        {{PYVENV_ON}} && {{PYVENV}} -m pre_commit install
    fi
    exit 0;

build-requirements:
    @echo "SUBTASK: build requirements"
    @just build-requirements-basics
    @just build-requirements-dependencies

build-requirements-basics:
    @{{PYVENV_ON}} && {{PYVENV}} -m pip install --upgrade pip
    @{{PYVENV_ON}} && {{PYVENV}} -m pip install --upgrade certifi wheel toml poetry

build-requirements-dependencies:
    @{{PYVENV_ON}} && {{PYVENV}} -m poetry lock --no-update
    @{{PYVENV_ON}} && {{PYVENV}} -m poetry install --no-interaction --no-root

build-models:
    @echo "SUBTASK: build data models from schemata."
    @just _delete-if-folder-exists "src/models/generated"
    @just _create-folder-if-not-exists "src/models/generated"
    @just _create-file-if-not-exists "src/models/generated/__init__.py"
    @just _generate-models-recursively "models" "src/models/generated"

build-docs:
    @echo "SUBTASK: build documentation for data models from schemata."
    @just _delete-if-folder-exists "docs/models"
    @just _create-folder-if-not-exists "docs/models"
    @- just _generate-documentation-recursively "models" "docs/models"
    @- just _clean-all-files "." ".openapi-generator*"
    @- just _clean-all-folders "." ".openapi-generator*"

build-archive:
    @echo "SUBTASK: build artefact"
    @mkdir -p dist
    @git archive --output "dist/${PROJECT_NAME}-$(cat dist/VERSION).zip" HEAD

# process for release
dist:
    @echo "TASK: create release"
    @just setup
    @just build
    @just build-docs
    @just build-archive

deploy-binary:
    #!/usr/bin/env bash

    # create zip artefact
    git add . && git commit --no-verify --allow-empty -m temp
    just build-archive
    git reset --soft HEAD~1 && git reset .

    VERSION="$(cat dist/VERSION)"
    FILE="dist/${PROJECT_NAME}-${VERSION}.zip"
    TARGET="${DEPLOYMENT_PATH}/bin"

    # zip -> binary
    mkdir -p "${TARGET}"
    cat "templates/template-app.py" | cat - "${FILE}" > "${TARGET}/${NAME_OF_APP}";
    chmod +x "${TARGET}/${NAME_OF_APP}";
    rm "dist/${PROJECT_NAME}-$(cat dist/VERSION).zip"
    exit 0;

deploy-open-source:
    #!/usr/bin/env bash

    # create zip artefact
    git add . && git commit --no-verify --allow-empty -m temp
    just build-archive
    git reset --soft HEAD~1 && git reset .

    VERSION="$(cat dist/VERSION)"
    FILE="dist/${PROJECT_NAME}-${VERSION}.zip"
    TARGET="${DEPLOYMENT_PATH}/${VERSION}"
    mkdir -p "${TARGET}"

    # unzip file in destination
    rm -rf "${TARGET}"
    unzip -q "${FILE}" -d "${TARGET}"
    cp -n .env "${TARGET}" 2> /dev/null

    # build repo there
    pushd "${TARGET}" >> /dev/null
        just setup
        just build-deployment
    popd >> /dev/null

    # create launch script
    TARGET="${DEPLOYMENT_PATH}/bin"
    mkdir -p "${TARGET}"
    CWD="{{PATH_ROOT}}"
    pushd "${TARGET}" >> /dev/null
        touch .env && rm .env
        echo "VERSION=\"${VERSION}\"" >> .env

        touch "${NAME_OF_APP}" && rm -f "${NAME_OF_APP}"
        cp "${CWD}/templates/template-app.sh" "${NAME_OF_APP}"

        chmod +x "${NAME_OF_APP}"
    popd >> /dev/null

    exit 0;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: execution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# DEV-NOTE:
# Together with 'set positional-arguments := true' above
# this is the way to preserve quotes in variadic arguments

run-cli *args:
    @{{PYVENV_ON}} && cd "{{CURRENT_DIR}}" && {{PYVENV}} "{{PATH_ROOT}}/src/main.py" "$@"

run-transpiler log_path="logs":
    @just _reset-logs
    @just run "run" "TRANSPILE" --logs "logs" --path "{{CURRENT_DIR}}"

examples log_path="logs":
    #!/usr/bin/env bash
    echo -e "CREATE EXAMPLES" >> /dev/stdout;
    just _reset-logs
    # loop through all files in examples folder
    while read path; do
        [[ "${path}" == "" ]] && continue;

        # create path for result
        path_output="$( echo "${path}" | sed -E "s/^examples\/example_/examples\/expected_/g" )";

        # copy example to results path
        rm -rf "${path_output}" 2> /dev/null;
        cp -r "$path/." "${path_output}";

        # run programme on example (in results path)
        just run --path "${path_output}" --log "{{log_path}}" "run" "TRANSPILE";
    done <<< $( find examples/example_* -mindepth 0 -maxdepth 0 2> /dev/null );
    exit 0;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: development
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Recipe only works if local file test.py exists
dev *args:
    @just _reset-logs
    @{{PYVENV_ON}} && {{PYVENV}} test.py "$@"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: tests
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

tests:
    @just tests-unit
    @just tests-behave
    @just tests-integration

tests-logs log_path="logs":
    @just _reset-logs "{{log_path}}"
    @- just tests
    @just _display-logs "{{log_path}}"

tests-unit:
    @just test-unit "tests/unit"

test-unit path="tests/unit" pattern="tests_ or test_":
    @just _reset-test-logs "unit"
    @{{PYVENV_ON}} && {{PYVENV}} -m pytest "{{path}}" \
        -k "{{pattern}}" \
        --cov-reset \
        --cov "src"

tests-behave full="false":
    @just test-behave "tests/behave" "{{full}}"

test-behave path full="false":
    @just _reset-test-logs "behave"
    @{{PYVENV_ON}} && {{PYVENV}} -m {{TOOL_TEST_BDD}} \
        --define sandbox-path-os="tests/behave/data" \
        --define full-tests="{{full}}" \
        --color \
        --show-timings \
        --no-capture \
        --no-logcapture \
        --tags ~@skip \
        --tags ~@TODO \
        --multiline \
        --summary \
        --stop \
        "{{path}}"

test-cases *args:
    @{{PYVENV_ON}} && {{PYVENV}} tests/cases/main.py "$@"

tests-integration log_path="logs":
    @just _reset-logs "{{log_path}}"
    @just test-cases run --no-inspect --log "{{log_path}}"

tests-integration-debug log_path="logs":
    @just _reset-logs "{{log_path}}"
    @just test-cases run --inspect --debug --log "{{log_path}}"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: qa
# NOTE: use for development only.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

qa:
    @{{PYVENV_ON}} && {{PYVENV}} -m coverage report -m

coverage source_path tests_path log_path="logs":
    @just _reset-logs "{{log_path}}"
    @{{PYVENV_ON}} && {{PYVENV}} -m pytest {{tests_path}} \
        --ignore=tests/integration \
        --cov-reset \
        --cov={{source_path}} \
        --capture=tee-sys \
        2> /dev/null
    @just _display-logs

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: prettify
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lint path:
    @{{PYVENV_ON}} && {{PYVENV}} -m {{LINTING}} --verbose "{{path}}"

lint-check path:
    @{{PYVENV_ON}} && {{PYVENV}} -m {{LINTING}} --check --verbose "{{path}}"

prettify:
    @{{PYVENV_ON}} && {{PYVENV}} -m {{LINTING}} --verbose *.py
    @{{PYVENV_ON}} && {{PYVENV}} -m {{LINTING}} --verbose src/*
    @{{PYVENV_ON}} && {{PYVENV}} -m {{LINTING}} --verbose tests/*

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: clean
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

clean log_path="logs":
    @- just clean-basic "{{log_path}}"
    @- just clean-venv

clean-basic log_path="logs":
    @echo "All system artefacts will be force removed."
    @- just _clean-all-files "." ".DS_Store" 2> /dev/null
    @echo "All test artefacts will be force removed."
    @- just _delete-if-folder-exists ".pytest_cache" 2> /dev/null
    @- just _delete-if-file-exists ".coverage" 2> /dev/null
    @- just _delete-if-folder-exists "tests/behave/logs" 2> /dev/null
    @echo "All execution artefacts will be force removed."
    @- just _delete-if-folder-exists "{{log_path}}" 2> /dev/null
    @echo "All build artefacts will be force removed."
    @- just _clean-all-folders "." ".idea" 2> /dev/null
    @- just _clean-all-folders "." "__pycache__" 2> /dev/null

clean-venv:
    @- just _delete-if-folder-exists ".venv" 2> /dev/null

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: logs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_clear-logs log_path="logs":
    @just _delete-if-folder-exists "{{log_path}}"

_create-logs log_path="logs":
    @just _create-logs-part "debug" "{{log_path}}"
    @just _create-logs-part "out" "{{log_path}}"
    @just _create-logs-part "err" "{{log_path}}"

_create-logs-part part log_path="logs":
    @just _create-folder-if-not-exists "{{log_path}}"
    @just _create-file-if-not-exists "{{log_path}}/{{part}}.log"

_reset-logs log_path="logs":
    @just _delete-if-folder-exists "{{log_path}}"
    @just _create-logs "{{log_path}}"

_reset-test-logs kind:
    @just _delete-if-folder-exists "tests/{{kind}}/logs"
    @just _create-logs-part "debug" "tests/{{kind}}/logs"

_display-logs log_path="logs":
    @echo ""
    @echo "Content of logs/debug.log:"
    @echo "----------------"
    @echo ""
    @- cat "{{log_path}}/debug.log"
    @echo ""
    @echo "----------------"

watch-logs n="10" log_path="logs":
    @tail -f -n {{n}} "{{log_path}}/out.log"

watch-logs-err n="10" log_path="logs":
    @tail -f -n {{n}} "{{log_path}}/err.log"

watch-logs-debug n="10" log_path="logs":
    @tail -f -n {{n}} "{{log_path}}/debug.log"

watch-logs-all n="10" log_path="logs":
    @just watch-logs {{n}} "{{log_path}}" &
    @just watch-logs-err {{n}} "{{log_path}}" &
    @just watch-logs-debug {{n}} "{{log_path}}" &

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: requirements
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

check-system:
    @echo "Operating System detected:  {{os_family()}}"
    @echo "Python command used:        ${PYTHON_PATH}"
    @echo "Python command for venv:    {{PYVENV}}"
    @echo "Python path for venv:       $( {{PYVENV_ON}} && which {{PYVENV}} )"

check-system-requirements:
    @just _check-python-tool "{{GEN_MODELS}}" "datamodel-code-generator"
    @just _check-tool "{{GEN_APIS}}" "openapi-code-generator"
    @just _check-python-tool "{{TOOL_TEST_BDD}}" "behave"
    @just _check-python-tool "{{LINTING}}" "{{LINTING}}"
    @just _check-python-tool "{{GITHOOK_PRECOMMIT}}" "pre-commit"
