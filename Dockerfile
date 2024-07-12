FROM --platform=${BUILDPLATFORM} rust:1-bookworm AS builder
ARG BUILDPLATFORM
ARG TARGETPLATFORM

WORKDIR /usr/src/royalnet/

RUN apt-get update && \
    apt-get upgrade --assume-yes

RUN \
    mkdir .cargo && \
    echo '[net]' >> .cargo/config.toml && \
    echo 'git-fetch-with-cli = true' >> .cargo/config.toml && \
    echo >> .cargo/config.toml && \
    if [ "${BUILDPLATFORM}" != "${TARGETPLATFORM}" ]; then \
        if [ "${TARGETPLATFORM}" = "linux/amd64" ]; then \
            dpkg --add-architecture amd64; \
            apt-get update; \
            apt-get install --assume-yes gcc-x86-64-linux-gnu; \
            echo '[target.x86_64-unknown-linux-gnu]' >> .cargo/config.toml; \
            echo 'linker = "x86-64-linux-gnu-gcc"' >> .cargo/config.toml; \
            echo >> .cargo/config.toml; \
        fi && \
        if [ "${TARGETPLATFORM}" = "linux/arm64" ]; then \
            dpkg --add-architecture arm64; \
            apt-get update; \
            apt-get install --assume-yes gcc-aarch64-linux-gnu; \
            echo '[target.aarch64-unknown-linux-gnu]' >> .cargo/config.toml; \
            echo 'linker = "aarch64-linux-gnu-gcc"' >> .cargo/config.toml; \
            echo >> .cargo/config.toml; \
        fi && \
        if [ "${TARGETPLATFORM}" = "linux/arm/v7" ]; then \
            dpkg --add-architecture armhf; \
            apt-get update; \
            apt-get install --assume-yes gcc-arm-linux-gnueabihf; \
            echo '[target.armv7-unknown-linux-gnueabihf]' >> .cargo/config.toml; \
            echo 'linker = "arm-linux-gnueabihf-gcc"' >> .cargo/config.toml; \
            echo >> .cargo/config.toml; \
        fi \
    fi

RUN \
    if [ "${TARGETPLATFORM}" = "linux/amd64" ]; then \
        RUSTTARGET=x86_64-unknown-linux-gnu; \
    fi && \
    if [ "${TARGETPLATFORM}" = "linux/arm64" ]; then \
        RUSTTARGET=aarch64-unknown-linux-gnu; \
    fi && \
    if [ "${TARGETPLATFORM}" = "linux/arm/v7" ]; then \
        RUSTTARGET=armv7-unknown-linux-gnueabihf; \
    fi && \
    rustup target add ${RUSTTARGET}

RUN \
    if [ "${TARGETPLATFORM}" = "linux/amd64" ]; then \
        apt-get install --assume-yes libpq5:amd64 libpq-dev:amd64 openssl:amd64 libssl-dev:amd64 pkg-config:amd64; \
    elif [ "${TARGETPLATFORM}" = "linux/arm64" ]; then \
        apt-get install --assume-yes libpq5:arm64 libpq-dev:arm64 openssl:arm64 libssl-dev:arm64 pkg-config:arm64; \
    elif [ "${TARGETPLATFORM}" = "linux/arm/v7" ]; then \
        apt-get install --assume-yes libpq5:armhf libpq-dev:armhf openssl:armhf libssl-dev:armhf pkg-config:armhf; \
    fi

COPY ./ ./

# This has reached a new level of hack
RUN \
    if [ "${TARGETPLATFORM}" = "linux/amd64" ]; then \
        RUSTTARGET=x86_64-unknown-linux-gnu; \
        export TARGET_CC=/usr/bin/x86-64-linux-gnu-gcc; \
        export TARGET_AR=/usr/bin/x86-64-linux-gnu-ar; \
        export PKG_CONFIG_PATH=/usr/x86-64-linux-gnu; \
    elif [ "${TARGETPLATFORM}" = "linux/arm64" ]; then \
        RUSTTARGET=aarch64-unknown-linux-gnu; \
        export TARGET_CC=/usr/bin/aarch64-linux-gnu-gcc; \
        export TARGET_AR=/usr/bin/aarch64-linux-gnu-ar; \
        export PKG_CONFIG_PATH=/usr/aarch64-linux-gnu; \
    elif [ "${TARGETPLATFORM}" = "linux/arm/v7" ]; then \
        RUSTTARGET=armv7-unknown-linux-gnueabihf; \
        export TARGET_CC=/usr/bin/arm-linux-gnueabihf-gcc; \
        export TARGET_AR=/usr/bin/arm-linux-gnueabihf-ar; \
        export PKG_CONFIG_PATH=/usr/arm-linux-gnueabihf; \
    fi && \
    cargo build --all-features --bins --release --target=${RUSTTARGET}


#############################################################################

FROM --platform=${TARGETPLATFORM} rust:1-slim-bookworm AS final

RUN apt-get update && \
    apt-get upgrade --assume-yes && \
    apt-get install --assume-yes libpq5 openssl

WORKDIR /usr/src/royalnet/
COPY --from=builder \
    /usr/src/royalnet/target/*/release/royalnet \
    /usr/bin/

ENTRYPOINT ["royalnet"]
CMD []

LABEL org.opencontainers.image.title="Royalnet"
LABEL org.opencontainers.image.description="Fun software suite for the RYG community"
LABEL org.opencontainers.image.licenses="EUPL-1.2"
LABEL org.opencontainers.image.url="https://github.com/RYGhub/royalnet"
LABEL org.opencontainers.image.authors="Stefano Pigozzi <me@steffo.eu>"
ENV RUST_LOG="warn,royalnet=info"
