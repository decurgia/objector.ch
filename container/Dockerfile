FROM python:3.12.4-alpine

ARG REQUIREMENTS=requirements-dev.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache git
COPY ./app /app/

WORKDIR /app/
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

CMD ["python", "objector/manage.py", "runserver", "0.0.0.0:8000"]