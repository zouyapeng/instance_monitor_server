#!/usr/bin/env python
# -*- coding: utf8 -*-
from trigger.models import Trigger, Event
from rest_framework import serializers


class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        fields = ('step_user', 'id', 'name', 'instance_uuid', 'item', 'item_option', 'period', 'method', 'method_option', 'threshold', 'status', 'contacts')


class EventSerializer(serializers.Serializer):
    pass
