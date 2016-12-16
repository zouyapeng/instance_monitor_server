#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.contrib import admin

from heartbeat.models import InstanceUUID, MonitorAgent
# Register your models here.


admin.site.register(InstanceUUID)
admin.site.register(MonitorAgent)
