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

RUN wget https://apt.llvm.org/llvm.sh \
    ./llvm.sh 13

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