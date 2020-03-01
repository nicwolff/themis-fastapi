FROM python:3.7.6-alpine3.11 AS base

###

FROM base AS build

RUN apk add -U gcc libc-dev make git postgresql-dev python-dev

WORKDIR /tmp

ENV PATH=/opt/local/bin:$PATH
ENV PIP_PREFIX=/opt/local
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ARG GITHUB_TOKEN
ARG GITHUB_AUTH_URL="https://$GITHUB_TOKEN:x-oauth-basic@github.com/Hearst"
RUN git config --global url.$GITHUB_AUTH_URL.insteadOf https://github.com/Hearst

COPY requirements.txt .
RUN pip install -r requirements.txt

###

FROM base AS deploy

RUN apk add -U bash

COPY --from=build /opt/local /opt/local
COPY --from=build /lib/libssl* /lib/libcrypto* /lib/
COPY --from=build /usr/lib/libpq* /usr/lib/libldap_r* /usr/lib/liblber* /usr/lib/libsasl2* /usr/lib/

WORKDIR /app
COPY . /app

# DO NOT TOUCH: Gets auto-updated by Ahab on release
ENV APP_VERSION=0.21.0
ENV APP_NAME="themis"

ENV PATH=/opt/local/bin:$PATH \
    PYTHONPATH=/opt/local/lib/python3.7/site-packages:/app/themis \
    GUNICORN_CMD_ARGS=$GUNICORN_CMD_ARGS \
    REDIS_HOST=$REDIS_HOST \
    REDIS_PORT=$REDIS_PORT \
    ENABLE_PARASITE=$ENABLE_PARASITE \
    APP_NAME=voltron

EXPOSE 80

STOPSIGNAL SIGINT

CMD ["ddtrace-run", "gunicorn", "-k uvicorn.workers.UvicornWorker", "--log-config=gunicorn_logging.conf", "-b 0.0.0.0:80", "themis.app:app"]
