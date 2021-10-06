################################################################
# !!! The following is an exmaple. Replace this by desired docker image instructions. !!!
FROM python:3.9.5-slim
#
################################################################

################################################################################
# START OF INSTRUCTIONS REQUIRED FOR WHALES PROJECT
# !!! The following lines are necessary for the Whales project !!!
# DEV-NOTE: Add `&& sleep 5` to lines, in order to see the console output.

# NOTE: some default values are sent from .whales scripts via --build-arg flag,
# but user can overwrite these with their own env-values + docker-compose.yml
ARG WHALES_SETUP_PATH
ARG WHALES_PROJECT_NAME
ARG WHALES_SELECTED_SERVICE

## Set whale-labels (used for searching):
LABEL org.whales.project="${WHALES_PROJECT_NAME}"
LABEL org.whales.service="${WHALES_SELECTED_SERVICE}"
LABEL org.whales.initial=true

ARG WD
COPY . "$WD"
WORKDIR "$WD"

# force whales + docker states (on, in):
RUN echo "on" >| "${WHALES_SETUP_PATH}/WHALES_STATE"
RUN echo "in" >| "${WHALES_SETUP_PATH}/DOCKER_STATE"
# add prefix to logging levels:
RUN echo "export LOGGINGPREFIX=\">\";" >> "${WHALES_SETUP_PATH}/.lib.globals.sh"

# END OF INSTRUCTIONS REQUIRED FOR WHALES PROJECT
################################################################################

# !!! Your build instructions here !!!
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y dos2unix
RUN apt-get install -y apt-utils
RUN apt-get install -y zip unzip xz-utils
RUN apt-get clean
