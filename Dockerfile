FROM ubuntu:14.04

MAINTAINER Zouyapeng<zyp19901009@163.com>

ADD https://github.com/zouyapeng/instance_monitor_server/archive/master.zip /

RUN unzip /instance_monitor_server-master.zip
