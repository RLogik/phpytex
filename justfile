# set shell := [ "bash", "-uc" ]
_default:
    @- just --unsorted --list
menu:
    @- just --unsorted --choose
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Justfile
# NOTE: Do not change the contents of this file!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_ROOT := justfile_directory()
CURRENT_DIR := invocation_directory()
PYTHON := if os_family() == "windows" { "py -3" } else { "python3" }
GEN_MODELS := "datamodel-codegen"
GEN_MODELS_DOCUMENTATION := "openapi-generator"
NAME_OF_APP := "phpytex"
PYTHON_APP_PREFIX := "#!/usr/bin/env python3\n-*- coding: utf-8 -*-"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Macros
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_create-file-if-not-exists fname:
    @touch "{{fname}}";

_create-folder-if-not-exists path:
    @if ! [ -d "{{path}}" ]; then mkdir -p "{{path}}"; fi

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

_delete-if-file-exists fname:
    @if [ -f "{{fname}}" ]; then rm "{{fname}}"; fi

_delete-if-folder-exists path:
    @if [ -d "{{path}}" ]; then rm -rf "{{path}}"; fi

_clean-all-files path pattern:
    @find {{path}} -type f -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    @- find {{path}} -type f -name "{{pattern}}" -exec rm {} \; 2> /dev/null

_clean-all-folders path pattern:
    @find {{path}} -type d -name "{{pattern}}" -exec basename {} \; 2> /dev/null
    @- find {{path}} -type d -name "{{pattern}}" -exec rm -rf {} \; 2> /dev/null

_check-tool tool name:
    #!/usr/bin/env bash
    if ( {{tool}} --version 2> /dev/null >> /dev/null ); then
        echo -e "Tool \x1b[2;3m{{name}}\x1b[0m installed correctly.";
        exit 0;
    else
        echo -e "Tool \x1b[2;3m{{tool}}\x1b[0m did not work." >> /dev/stderr;
        echo -e "Ensure that \x1b[2;3m{{name}}\x1b[0m (-> \x1b[1mjust build\x1b[0m) installed correctly and system paths are set." >> /dev/stderr;
        exit 1;
    fi

_check-python-tool tool name:
    #!/usr/bin/env bash
    success=false
    {{tool}} --help >> /dev/null 2> /dev/null && success=true;
    # NOTE: if exitcode is 251 (= help or print version), then render success.
    [[ "$?" == "251" ]] && success=true;
    # FAIL tool not installed
    if ( $success ); then
        echo -e "Tool \x1b[2;3m{{name}}\x1b[0m installed correctly.";
        exit 0;
    else
        echo -e "Tool \x1b[2;3m{{tool}}\x1b[0m did not work." >> /dev/stderr;
        echo -e "Ensure that \x1b[2;3m{{name}}\x1b[0m (-> \x1b[1mjust build\x1b[0m) installed correctly and system paths are set." >> /dev/stderr;
        exit 1;
    fi

_generate-models path name:
    @{{GEN_MODELS}} \
        --input-file-type openapi \
        --encoding "UTF-8" \
        --disable-timestamp \
        --use-schema-description \
        --field-constraints \
        --set-default-enum-member \
        --allow-population-by-field-name \
        --snake-case-field \
        --strict-nullable \
        --target-python-version 3.10 \
        --input {{path}}/{{name}}-schema.yaml \
        --output {{path}}/generated/{{name}}.py

_generate-models-documentation path_schema path_docs name:
    @- {{GEN_MODELS_DOCUMENTATION}} generate \
        --skip-validate-spec \
        --input-spec {{path_schema}}/{{name}}-schema.yaml \
        --generator-name markdown \
        --output "{{path_docs}}/{{name}}"

_build-models-recursively models_path:
    #!/usr/bin/env bash
    just _delete-if-folder-exists "{{models_path}}/generated"
    just _create-folder-if-not-exists "{{models_path}}/generated"
    just _create-file-if-not-exists "{{models_path}}/generated/__init__.py"
    while read path; do
        if [[ "${path}" == "" ]]; then continue; fi
        path="${path##*/}";
        name="$( echo """${path}""" | sed -E """s/^(.*)-schema\.yaml$/\1/g""")";
        just _generate-models "{{models_path}}" "$name";
    done <<< "$( ls -f {{models_path}}/*-schema.yaml )";

_build-documentation-recursively models_path documentation_path:
    #!/usr/bin/env bash
    while read path; do
        if [[ "${path}" == "" ]]; then continue; fi
        path="${path##*/}";
        name="$( echo """${path}""" | sed -E """s/^(.*)-schema\.yaml$/\1/g""")";
        just _generate-models-documentation "{{models_path}}" "{{documentation_path}}" "$name";
    done <<< "$( ls -f {{models_path}}/*-schema.yaml )";

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: build
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

build:
    @just build-requirements
    @just check-system-requirements
    @just build-models
build-requirements:
    @{{PYTHON}} -m pip install --disable-pip-version-check -r requirements.txt
build-models:
    @echo "Generate data models from schemata."
    @- just _build-models-recursively "src/models"
    @- just _build-models-recursively "tests/models"
build-documentation:
    @echo "Generate documentations data models from schemata."
    @just _delete-if-folder-exists "documentation"
    @just _create-folder-if-not-exists "documentation"
    @- just _build-documentation-recursively "src/models" "documentation/app"
    @- just _build-documentation-recursively "tests/models" "documentation/tests"
    @- just _clean-all-files "." ".openapi-generator*"
    @- just _clean-all-folders "." ".openapi-generator*"
build-examples:
    #!/usr/bin/env bash
    echo "CREATE EXAMPLES";
    while read path; do
        if [[ "${path}" == "" ]]; then continue; fi
        sandboxpath="$( echo "${path}" | sed -E "s/^examples\/example_/examples\/expected_/g" )";
        if [[ "${path}" == "${sandboxpath}" ]]; then continue; fi
        if [[ -d "${sandboxpath}" ]]; then rm -rf "${sandboxpath}"; fi
        echo "${sandboxpath}"
        cp -r "${path}/." "${sandboxpath}";
        pushd "${sandboxpath}" >> /dev/null;
            {{PATH_ROOT}}/dist/{{NAME_OF_APP}} run;
        popd >> /dev/null;
    done <<< $( ls -d examples/example_* 2> /dev/null );
build-artefact:
    #!/usr/bin/env bash
    echo "CREATE ARTEFACT";

    # first copy to temp directory
    _temp="$( just _create-temp-folder """dist""" )";

    # copy in the relevant files
    cp -r "src" "${_temp}";
    cp -r "assets" "${_temp}";
    mkdir -p "${_temp}/dist"
    cp "dist/VERSION" "${_temp}/dist";
    mv "${_temp}/src/__main__.py" "$_temp";
    rm "${_temp}/src/paths.py";
    mv "${_temp}/src/__paths__.py" "${_temp}/src/paths.py";

    # zip source files to single file and make executable:
    success=1;
    pushd "$_temp" >> /dev/null
        zip -r -o "{{PATH_ROOT}}/dist/app.zip" * -x '*__pycache__/*' -x '*.DS_Store' 2> /dev/null;
        success=$?;
    popd >> /dev/null
    if [[ ${success} -eq 0 ]]; then
        echo  "{{PYTHON_APP_PREFIX}}" | cat - dist/app.zip > dist/{{NAME_OF_APP}};
        chmod +x "dist/{{NAME_OF_APP}}";
    fi

    # remove temp artefacts:
    rm -rf "${_temp}";
    rm "dist/app.zip";
    if [[ ${success} -eq 0 ]]; then
        echo -e "Python artefact successfully created.";
    else
        echo -e "Creation of artefact failed.";
    fi

# process for release
dist:
    @just clean
    @just build
    @just build-documentation
    @# just build-examples
    @just build-artefact

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: run
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

run:
    @{{PYTHON}} src/main.py run;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: tests
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

tests:
    @- just tests-unit
    @- just tests-integration
tests-logs:
    @just _create-logs
    @- just tests
    @just _display-logs
tests-inspect: tests-unit tests-integration-inspect
tests-unit:
    @{{PYTHON}} -m pytest tests \
        --ignore=tests/integration \
        --cov-reset \
        --cov=. \
        2> /dev/null
tests-unit-logs:
    @just _create-logs
    @- just tests-unit
    @just _display-logs
tests-integration:
	@{{PYTHON}} tests/main.py run --quiet --plain
tests-integration-inspect:
	@{{PYTHON}} tests/main.py run --inspect

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: qa
# NOTE: use for development only.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

qa:
    @{{PYTHON}} -m coverage report -m
coverage source_path tests_path:
    @just _create-logs
    @-just _coverage-no-logs "{{source_path}}" "{{tests_path}}"
    @just _display-logs
_coverage-no-logs source_path tests_path:
    @{{PYTHON}} -m pytest {{tests_path}} \
        --ignore=tests/integration \
        --cov-reset \
        --cov={{source_path}} \
        --capture=tee-sys \
        2> /dev/null

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: clean
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

clean:
    @echo "All system artefacts will be force removed."
    @- just _clean-all-files "." ".DS_Store" 2> /dev/null
    @echo "All test artefacts will be force removed."
    @- just _clean-all-folders "." ".pytest_cache" 2> /dev/null
    @- just _delete-if-file-exists ".coverage" 2> /dev/null
    @- just _delete-if-folder-exists "logs"
    @echo "All build artefacts will be force removed."
    @- just _clean-all-folders "." "__pycache__" 2> /dev/null
    @- just _delete-if-folder-exists "models/generated" 2> /dev/null
    @- just _delete-if-file-exists "dist/{{NAME_OF_APP}}" 2> /dev/null

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: logging, session
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_create-logs:
    @# For logging purposes (since stdout is rechanneled):
    @just _delete-if-file-exists "logs/debug.log"
    @just _create-folder-if-not-exists "logs"
    @just _create-file-if-not-exists "logs/debug.log"
_display-logs:
    @echo ""
    @echo "Content of logs/debug.log:"
    @echo "----------------"
    @echo ""
    @- cat logs/debug.log
    @echo ""
    @echo "----------------"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TARGETS: requirements
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

check-system:
    @echo "Operating System detected: {{os_family()}}."
    @echo "Python command used: {{PYTHON}}."
check-system-requirements:
    @just _check-python-tool "{{GEN_MODELS}}" "datamodel-code-generator"
    @just _check-python-tool "{{GEN_MODELS_DOCUMENTATION}}" "openapi-code-generator"
