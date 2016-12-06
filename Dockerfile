FROM ubuntu:14.04
MAINTAINER Zouyapeng<zyp19901009@163.com>

ENV DJANGO_VERSION 1.8.4

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
		python-pip \
		unzip \
		python-dev \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN pip install mysqlclient psycopg2 django=="$DJANGO_VERSION" uwsgi pymongo==3.4.0

ADD https://github.com/zouyapeng/instance_monitor_server/archive/master.zip /
#RUN unzip /instance_monitor_server-master.zip

#WORKDIR /instance_monitor_server


