FROM python:3.8.13-slim

COPY . /sos-robot

WORKDIR /sos-robot

RUN pip install --no-cache-dir -r requirements.txt