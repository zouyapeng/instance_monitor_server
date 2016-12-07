FROM ubuntu:14.04
MAINTAINER Zouyapeng<zyp19901009@163.com>

ENV \
    OPENSTACK_AUTH_URL=172.23.4.1 \
    DB_HOSTNAME=vmserverdb \
    DB_USER=vmserver \
    DB_PASSWORD=vmserver

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
	--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -fr /tmp/* \
    && rm -fr /var/tmp/*

COPY supervisor-app.conf /etc/supervisor/conf.d/

ADD https://github.com/zouyapeng/instance_monitor_server/archive/master.zip /home/
RUN unzip /home/master.zip -d /home \
    && pip install -r /home/instance_monitor_server-master/requestments.txt

RUN sed -i "s/127.0.0.1/$OPENSTACK_AUTH_URL/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py \
    && sed -i "s/'NAME':.*,/'NAME': '$DB_HOSTNAME',/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py \
    && sed -i "s/'USER':.*,/'USER': '$DB_USER',/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py \
    && sed -i "s/'PASSWORD':.*,/'PASSWORD': '$DB_PASSWORD',/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py

ENTRYPOINT ["/bin/sleep 30s", "&&", "supervisord", "-n"]