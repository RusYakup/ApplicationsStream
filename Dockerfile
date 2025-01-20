FROM python:3.12-slim-bookworm AS builder
LABEL maintainer="rustam-dev"
WORKDIR /app
COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip
RUN pip install --timeout=120 pipenv
RUN pipenv install --system

COPY . .