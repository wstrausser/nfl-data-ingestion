FROM python:latest

COPY . /schedule_ingestion

RUN yes | apt update
RUN yes | apt upgrade

RUN yes | apt install libsnappy-dev
RUN yes | pip install /schedule_ingestion
