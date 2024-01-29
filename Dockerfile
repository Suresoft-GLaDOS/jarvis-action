FROM ubuntu:20.04
ARG llvmver=10

ENV ACTION_CALL=TRUE
ENV PATH=/home/workspace/tbeg/apps/csbuild-ubuntu-20.04_v1.2.0/bin:$PATH

ENV TZ=Asia/Kolkata \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install tzdata

RUN apt update
RUN apt install -y vim binutils gcc g++ make python3 git
RUN apt-get -y install python3-pip
RUN apt-get -y install autoconf pkg-config libtool
RUN apt-get -y install cppcheck
RUN apt-get -y install dos2unix
RUN apt-get update \
    && apt-get install -y \
    software-properties-common \
    gnupg \
    # Needed for repo access
    apt-transport-https \
    ca-certificates

RUN apt-get update && apt-get install -y \
 xz-utils \
 curl \
 && rm -rf /var/lib/apt/lists/*

ARG LLVM_DIR=/opt/llvm
ARG LLVM_VERSION="11.1.0"
RUN git clone https://github.com/llvm/llvm-project.git /tmp/llvm \
    && cd /tmp/llvm \
    && git checkout "llvmorg-${LLVM_VERSION}" \
    && cd /tmp/llvm \
    && mkdir build \
    && cd build \
    && cmake \
        -DCMAKE_INSTALL_PREFIX="${LLVM_DIR}" \
        -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;libcxx;libcxxabi;compiler-rt" \
        -DCMAKE_BUILD_TYPE=Release \
        -DLLVM_ENABLE_ASSERTIONS=true \
        -DLLVM_ENABLE_RTTI=true \
        -DLLVM_PARALLEL_LINK_JOBS=1 \
        -G Ninja \
        ../llvm \
    && ninja \
    && ninja install \
    && rm -rf /tmp/llvm
ENV PATH "${LLVM_DIR}/bin:${PATH}"

RUN type -p curl >/dev/null || (apt update && apt install curl -y)
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt update \
    && apt install gh -y

RUN pip install python-dotenv openai pyfiglet gitpython
RUN pip install clang libclang

RUN useradd --home-dir /home/workspace jarvis

WORKDIR /home/workspace