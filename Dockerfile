FROM ubuntu:14.04
MAINTAINER Zouyapeng<zyp19901009@163.com>

ENV \
    OPENSTACK_AUTH_URL=127.0.0.1 \
    DB_NAME=vmserver \
    DB_USER=vmserver \
    DB_PASSWORD=vmserver \
    MONGODB_HOST=192.168.213.230 \
    MONGODB_PORT=27017 \
    MONGODB_EXPIRE=2592000

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
		sqlite3 \
		python-pip \
		unzip \
		python-dev \
		supervisor \
		python-mysqldb \
	--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -fr /tmp/* \
    && rm -fr /var/tmp/*

COPY supervisor-app.conf /etc/supervisor/conf.d/

ADD https://github.com/zouyapeng/instance_monitor_server/archive/master.zip /home/
RUN unzip /home/master.zip -d /home \
    && pip install -r /home/instance_monitor_server-master/requestments.txt

ENTRYPOINT ["/home/instance_monitor_server-master/run.sh"]