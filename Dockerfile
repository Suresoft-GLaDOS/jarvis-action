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

ADD llvm.list /
ADD llvm-snapshot.gpg.key /

# Install pre-reqs
RUN  mv llvm.list /etc/apt/sources.list.d/ \
    && apt-key add llvm-snapshot.gpg.key \
    && rm llvm-snapshot.gpg.key \
    && apt-get update \
    && apt-get install -y \
    build-essential \
    # Install Tool
    clang-$llvmver \
    clang-tools-$llvmver \
    clang-format-$llvmver \
    python3-clang-$llvmver \
    libfuzzer-$llvmver-dev \
    lldb-$llvmver \
    lld-$llvmver \
    libc++-$llvmver-dev \
    libc++abi-$llvmver-dev \
    libomp-$llvmver-dev \
    # Make an alias for the versioned executable
    && ln -s /usr/bin/clang++-$llvmver /usr/bin/clang++ \
    && ln -s /usr/bin/clang-$llvmver /usr/bin/clang

RUN type -p curl >/dev/null || (apt update && apt install curl -y)
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt update \
    && apt install gh -y

RUN pip install python-dotenv openai pyfiglet gitpython

RUN useradd --home-dir /home/workspace jarvis

WORKDIR /home/workspace