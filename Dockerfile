FROM python:2.7-slim
MAINTAINER Zouyapeng<zyp19901009@163.com>

ADD https://github.com/zouyapeng/instance_monitor_server/archive/master.zip /
RUN unzip /instance_monitor_server-master.zip

WORKDIR /instance_monitor_server

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV DJANGO_VERSION 1.8.4

RUN pip install mysqlclient psycopg2 django=="$DJANGO_VERSION"
