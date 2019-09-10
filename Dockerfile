FROM alpine:3.10

MAINTAINER path-help@sanger.ac.uk

ENV  BUILD_DIR /tmp/baker-install

# Copy repo content into container
RUN  mkdir -p ${BUILD_DIR}
COPY . ${BUILD_DIR}

RUN echo "**** install bash ****" && \
    apk add --no-cache bash

RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN cd "${BUILD_DIR}" && \
    pip install . && \
    rm -rf "${BUILD_DIR}"
