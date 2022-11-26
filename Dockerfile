FROM python:3.11-alpine
WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ .
ARG PYTHONPATH=/app/
