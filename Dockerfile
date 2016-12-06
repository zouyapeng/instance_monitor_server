FROM ubuntu:14.04
MAINTAINER Zouyapeng<zyp19901009@163.com>

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
RUN unzip /home/master.zip -d /home

RUN pip install -r /home/instance_monitor_server-master/requestments.txt

#CMD ["/usr/local/bin/uwsgi", "/home/instance_monitor_server-master/uwsgi.ini"]
CMD ["supervisord", "-n"]