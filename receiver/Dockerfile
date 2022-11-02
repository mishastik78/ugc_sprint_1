FROM python:3.11.0-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY src/. /usr/app

ENTRYPOINT /usr/local/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
