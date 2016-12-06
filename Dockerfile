FROM ubuntu:14.04
MAINTAINER Zouyapeng<zyp19901009@163.com>

ENV \
    DJANGO_VERSION=1.8.4 \
    LISTEN_PORT=9338

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
		sqlite3 \
		python-pip \
		unzip \
		python-dev \
		nginx \
		supervisor \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

ADD https://github.com/zouyapeng/instance_monitor_server/archive/master.zip /home/
RUN unzip /home/master.zip -d /home

RUN pip install -r /home/instance_monitor_server-master/requestments.txt

RUN echo "daemon off;" >> /etc/nginx/nginx.conf && \
        cp /home/instance_monitor_server-master/VMServer.conf /etc/nginx/conf.d/ && \
        cp /home/instance_monitor_server-master/supervisor-app.conf /etc/supervisor/conf.d/

EXPOSE 9339

ENTRYPOINT ["supervisord"]

CMD ["-n"]