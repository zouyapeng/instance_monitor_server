#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.contrib import admin
from trigger.models import Trigger, Event

# Register your models here.
admin.site.register(Trigger)
admin.site.register(Event)