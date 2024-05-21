# syntax=docker/dockerfile:1
FROM python:3.12.3

WORKDIR /app

ARG REQUIREMENTS=requirements-dev.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y gettext postgresql-client && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*

COPY requirements.txt requirements-dev.txt /app/
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

COPY . /app/
