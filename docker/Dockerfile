# syntax=docker/dockerfile:1

FROM ghcr.io/linuxserver/baseimage-alpine:3.24 AS builder

ARG BUILD_DATE
ARG VERSION
LABEL build_version="Linuxserver.io version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="felix2yu"

ENV PYTHONUNBUFFERED=1

RUN \
  echo "**** install build packages ****" && \
  apk add --no-cache --virtual=build-dependencies \
    build-base \
    cargo \
    curl-dev \
    jpeg-dev \
    libffi-dev \
    mariadb-dev \
    musl-dev \
    postgresql-dev \
    python3-dev \
    zlib-dev && \
  echo "**** install runtime packages ****" && \
  apk add --no-cache \
    grep \
    mariadb-client \
    postgresql-client \
    python3 \
    uwsgi \
    uwsgi-python \
    mariadb-connector-c && \
  echo "**** create python virtualenv ****" && \
  python3 -m venv /lsiopy && \
  pip install -U --no-cache-dir \
    pip \
    wheel

COPY requirements.txt /tmp/
RUN \
  . /lsiopy/bin/activate && \
  pip install -U --no-cache-dir \
    apprise \
    minio \
    mysqlclient && \
  pip install -U --no-cache-dir -r /tmp/requirements.txt

COPY . /app/healthchecks/

RUN cd /app/healthchecks && \
    rm -rf .git stuff && \
    . /lsiopy/bin/activate && \
    DEBUG=False SECRET_KEY=build-key python3 ./manage.py collectstatic --noinput && \
    DEBUG=False SECRET_KEY=build-key python3 ./manage.py compress

RUN \
  echo "**** cleanup ****" && \
  apk del --purge \
    build-dependencies && \
  rm -rf \
    /root/.cache \
    /root/.cargo \
    /tmp/*

FROM ghcr.io/linuxserver/baseimage-alpine:3.24

ENV PYTHONUNBUFFERED=1

RUN \
  apk add --no-cache \
    grep \
    mariadb-client \
    postgresql-client \
    python3 \
    uwsgi \
    uwsgi-python \
    mariadb-connector-c

COPY --from=builder /lsiopy /lsiopy
COPY --from=builder /app/healthchecks /app/healthchecks

COPY docker/root/ /

RUN chmod +x \
    /etc/s6-overlay/s6-rc.d/init-healthchecks-config/run \
    /etc/s6-overlay/s6-rc.d/svc-healthchecks/run

EXPOSE 8000

VOLUME /config
