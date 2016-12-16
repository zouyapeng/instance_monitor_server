#!/usr/bin/env python
# -*- coding: utf8 -*-

from trigger.models import Trigger, Event
from trigger.serializers import TriggerSerializer, EventSerializer
from trigger.tasks import send_email, send_sms
from rest_framework import generics
from rest_framework.response import Response
from django.conf import settings

import datetime


class TriggerListView(generics.CreateAPIView):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer

    def post(self, request, *args, **kwargs):
        step_user = request.data.get('step_user', None)
        if step_user is None:
            return Response(data={'detail': 'step_user is need for get trigger list.'}, status=400)

        queryset = Trigger.objects.filter(step_user=step_user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class TriggerCreateView(generics.CreateAPIView):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer


class TriggerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer

    def put(self, request, *args, **kwargs):
        trigger = self.get_object()
        request_status = request.data.get('status')
        if trigger.status != request_status:
            if request_status is True:
                try:
                    Event.objects.get(trigger=trigger, status=True)
                except Event.DoesNotExist:
                    event = Event(trigger=trigger, status=True)
                    event.save()
                    send_sms.delay(event)
                    send_email.delay(event)
            else:
                try:
                    event = Event.objects.get(trigger=trigger, status=True)
                    event.end_time = datetime.datetime.now()
                    event.status = False
                    event.save()
                except Event.DoesNotExist:
                    pass

        return super(TriggerRetrieveUpdateDestroyView, self).put(request, args, kwargs)


class EventListView(generics.CreateAPIView):
    queryset = []
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        events = []
        uuids = request.data.get('uuids', None)
        for uuid in uuids:
            triggers = Trigger.objects.filter(instance_uuid=uuid)
            for trigger in triggers:
                events.extend(trigger.get_events())

        return Response(events)