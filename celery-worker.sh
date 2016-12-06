#!/bin/bash

nohup python /home/instance_monitor_server-master/manage.py celery worker --beat > /dev/null 2>&1 &
