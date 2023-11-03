FROM python:latest

COPY . /app

RUN yes | apt update
RUN yes | apt upgrade

RUN yes | apt install libsnappy-dev
RUN yes | pip install /app

ENTRYPOINT ["/app/scripts/update.py"]
