FROM ubuntu:18.04

MAINTAINER path-help@sanger.ac.uk

ARG DEBIAN_FRONTEND=noninteractive

ARG BUILD_DIR=/tmp/baker-install

ARG SINGULARITY_VERSION=3.4.0

# Ubuntu
RUN apt-get update -qq -y && \
    apt-get upgrade -qq -y

# Dependencies for singularity and python
RUN apt-get update -qq -y && \
    apt-get install -qq -y \
    build-essential \
    libssl-dev \
    uuid-dev \
    libgpgme11-dev \
    squashfs-tools \
    libseccomp-dev \
    wget \
    pkg-config \
    git \
    python3 \
    python3-pip \
    software-properties-common \
    cryptsetup-bin \
    uidmap

# Go
RUN add-apt-repository ppa:longsleep/golang-backports && \
    apt-get update -qq -y && \
    apt-get install golang-go  -qq -y

# Singularity
RUN mkdir /tmp/singularity && \
    cd /tmp/singularity && \
    wget -q https://github.com/sylabs/singularity/releases/download/v${SINGULARITY_VERSION}/singularity-${SINGULARITY_VERSION}.tar.gz && \
    tar -xf singularity-${SINGULARITY_VERSION}.tar.gz && \
    cd singularity && \
    ./mconfig && \
    make -C builddir && \
    make -C builddir install && \
    cd /tmp && \
    rm -rf /tmp/singularity

# Baker
COPY . "${BUILD_DIR}"
RUN cd "${BUILD_DIR}" && \
    pip3 install . && \
    rm -rf "${BUILD_DIR}"
