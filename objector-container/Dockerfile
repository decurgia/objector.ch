FROM python:3.12.4-alpine

ARG REQUIREMENTS=requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system app && adduser --system app app
RUN apk add --no-cache git
COPY ./app /app/

WORKDIR /app/
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

RUN chown -R app:app /app/
USER app

CMD ["python", "objector/manage.py", "runserver", "0.0.0.0:8081"]
