FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /etu_flow
WORKDIR /etu_flow

RUN apt-get update && apt-get install gcc -y
RUN apt-get install libpq-dev -y
RUN chmod +x /etu_flow/entrypoint.sh
RUN python -m pip install pip==23.0.1 && pip install -r requirements.txt

ENTRYPOINT ["/etu_flow/entrypoint.sh"]

