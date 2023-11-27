FROM ubuntu:20.04

ENV ACTION_CALL=TRUE
ENV PATH=/home/workspace/tbeg/apps/csbuild-ubuntu-20.04_v1.2.0/bin:$PATH

ENV TZ=Asia/Kolkata \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install tzdata

RUN apt update
RUN apt install -y vim binutils gcc g++ make python3 git
RUN apt-get -y install python3-pip dos2unix
RUN apt-get -y install autoconf pkg-config libtool

RUN type -p curl >/dev/null || (apt update && apt install curl -y)
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt update \
    && apt install gh -y

RUN pip install python-dotenv openai pyfiglet gitpython

RUN useradd --home-dir /home/workspace jarvis

WORKDIR /home/workspace