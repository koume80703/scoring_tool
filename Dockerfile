FROM openjdk:11-slim

LABEL maintainer="kohei_lab"
LABEL description="java_python_env"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ="Asia/Tokyo"
ENV TERM="xterm-color"

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y git nkf

RUN mkdir -p /home/
COPY requirements.txt /home/
WORKDIR /home/

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install -r requirements.txt