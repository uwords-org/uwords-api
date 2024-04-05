FROM python:3.11-slim

WORKDIR /backend

ENV PYTHONUNBUFFERED=0
ENV DJANGO_SETTINGS_MODULE=uwords_api.settings

COPY requirements.txt .

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . .