#!/bin/bash

sed -i "s/OPENSTACK_AUTH_URL=.*/OPENSTACK_AUTH_URL='http:\/\/$OPENSTACK_AUTH_URL:5000\/v2.0\/'/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py
sed -i "s/'NAME':.*,/'NAME': '$DB_NAME',/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py
sed -i "s/'USER':.*,/'USER': '$DB_USER',/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py
sed -i "s/'PASSWORD':.*,/'PASSWORD': '$DB_PASSWORD',/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py
sed -i "s/MONGODB_HOST=.*/MONGODB_HOST='$MONGODB_HOST'/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py
sed -i "s/MONGODB_PORT=.*/MONGODB_PORT=$MONGODB_PORT/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py
sed -i "s/MONGODB_EXPIRE=.*/MONGODB_EXPIRE=$MONGODB_EXPIRE/g" /home/instance_monitor_server-master/instance_monitor_server/settings.py

sleep 30s;
supervisord -n