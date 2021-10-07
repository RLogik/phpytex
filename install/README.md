# Installation of Phpytex #

The programme can either be installed from the artefacts or from the source code.

## Installation via artefacts ##

The script [install/installphpytex](./installphpytex) allows users to easily install
and maintain Phpytex versions from the git repository in a uniform manner.
It also allows users to switch between versions.

### Steps ###

Steps 1–3 theoretically only need to be performed once.
(Step 1 may need repeating, if the install script is updated in future versions of Phpytex.)

1. Copy thie script to a folder on your system where local binaries are kept.

2. Within this path call
    ```bash
    chmod +x installphpytex
    ```
    to grant the script execution rights.

3. If you do not already have a user bash profile, create this via the bash command
    ```bash
    touch $HOME/.bash_profile
    ```
    then add the
    ```bash
    export PATH="$HOME/.phpytex/bin:${PATH}";
    ```
    to your **.bash_profile**.

4. You can now call `installphpytex` anywhere on your system.
    <br/>
    For example you can call
    ```bash
    installphpytex --git vX.Y.Z
    ```
    to download, install, and link version `X.Y.Z` of Phpytex to the command **phpytex**.
    Or you can call
    ```bash
    installphpytex vX.Y.Z
    ```
    to link version `X.Y.Z` to the **phpytex** command, provided you have already installed this version.
    <br/>
    Call `installphpytex --help` for a full guide on usage.

5. Provided that Step 3 above was completed, call
    ```bash
    phpytex version
    ```
    to verify that the correct version of Phpytex is linked to the **phpytex** command.

## Installation from source ##

1. Clone this repository

2. Open a bash console (on Windows install [bash for windows](https://gitforwindows.org))
   and change the directory to the root directory of this project.

3. Call
    ```bash
    chmod +x scripts/*.sh; # or simply chmod +x scripts/build.sh
    ```
    That grants the process scripts execution rights.

4. Run the setup process without venv (installs necessary python packages) via
    ```bash
    ./scripts/build.sh --mode setup --venv false
    ```

5. Run the distribution process (compresses the source folder to an runnable zip file)
    ```bash
    ./scripts/build.sh --mode dist
    ```
    to create the binary.

6. Copy this binary to a folder with local binaries on your system (_e.g._ `/usr/local/bin` on OSX),
    and grant the script execution rights via `chmod +x path/to/file`.

7. Provided the above steps were successful call
    ```bash
    phpytex version
    ```
    to verify that Phpytex (and the correct version) is linked to the **phpytex** command.
