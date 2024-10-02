FROM alpine:latest

RUN apk update && apk add --no-cache \
    g++ \
    cmake \
    openssl-dev \
    git \
    bash \
    iproute2 \
    net-tools \
    rsync \
    openrc \
    make \
    build-base

RUN mkdir -p /opt/mundfish/

ENV DRM_DIR="/opt/mundfish/" \
    SOURCE_DIR="/opt/mundfish/" \
    REPO_URL="your_git_token"

RUN git clone --recursive $REPO_URL $DRM_DIR
WORKDIR $DRM_DIR
RUN git pull
WORKDIR $SOURCE_DIR
RUN cmake -DCMAKE_BUILD_TYPE=Release . && cmake --build .
WORKDIR $SOURCE_DIR/bin/
RUN chmod +x ./drm

EXPOSE 19696 9696

CMD ["your_executable_file"]