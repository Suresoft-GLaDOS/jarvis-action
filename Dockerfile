FROM ubuntu:20.04

ENV ACTION_CALL=TRUE
ENV PATH=/home/workspace/tbeg/apps/csbuild-ubuntu-20.04_v1.2.0/bin:$PATH

RUN apt update
RUN apt install -y vim binutils gcc g++ make python3 git
RUN apt-get -y install python3-pip

RUN pip install python-dotenv openai pyfiglet

RUN useradd --home-dir /home/workspace jarvis

WORKDIR /home/workspace