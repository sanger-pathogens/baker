FROM ubuntu:18.04

MAINTAINER path-help@sanger.ac.uk

ARG DEBIAN_FRONTEND=noninteractive

ARG BUILD_DIR=/tmp/baker-install

# Ubuntu
RUN apt-get update -qq -y \
    && apt-get upgrade -qq -y

# Dependencies for singularity and python
RUN apt-get update -qq -y \
    && apt-get install -qq -y \
      python3 \
      python3-pip

# Baker
COPY . "${BUILD_DIR}"
RUN cd "${BUILD_DIR}" \
    && pip3 install . \
    && rm -rf "${BUILD_DIR}"
