#!/usr/bin/env python
# -*- coding: utf8 -*-

from celery.task import task
from heartbeat.models import MonitorAgent
import datetime


@task()
def check_agent_status():
    logger = check_agent_status.get_logger()
    last_lost_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
    agents = MonitorAgent.objects.filter(update_time__lt=last_lost_time, status=True)
    for agent in agents:
        logger.info("%s Have going to Inactive!" % agent.hostname)
        agent.status = False
        agent.save()

