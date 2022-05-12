# FROM python:3
FROM openjdk:11-slim

LABEL maintainer="kohei_lab"
LABEL description="java_python_env"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ="Asia/Tokyo"
ENV TERM="xterm-color"

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y nkf

RUN mkdir -p /root/src
COPY requirements.txt /root/src
WORKDIR /root/src

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install -r requirements.txt