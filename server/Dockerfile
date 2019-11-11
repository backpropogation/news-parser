FROM python:3.7-slim

RUN mkdir /server && apt-get update && apt-get install -y git
WORKDIR /server

COPY ./server/requirements.txt /server/requirements.txt

COPY ./server /server

RUN pip install -r requirements.txt
