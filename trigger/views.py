
from trigger.models import Trigger
from heartbeat.models import InstanceUUID
from trigger.serializers import TriggerSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.conf import settings


class TriggerListCreateView(generics.ListCreateAPIView):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer

    def get(self, request, *args, **kwargs):
        triggers = super(TriggerListCreateView, self).get(request, args, kwargs)
        return triggers

    def post(self, request, *args, **kwargs):
        instance_uuid = request.data.get('instance_uuid')
        try:
            uuid = InstanceUUID.objects.get(uuid=instance_uuid)
            request.data['instance_uuid'] = uuid.id
        except InstanceUUID.DoesNotExist:
            pass

        return super(TriggerListCreateView, self).post(request, args, kwargs)


class TriggerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer

    def put(self, request, *args, **kwargs):
        return super(TriggerRetrieveUpdateDestroyView, self).put(request, args, kwargs)


class EventListView(generics.CreateAPIView):
    queryset = []

    def post(self, request, *args, **kwargs):
        events = []
        uuids = request.data.get['uuids']
        for uuid in uuids:
            events.extend(Trigger.objects.get(instance_uuid=uuid).get_problem_events())

        return Response({'events': events})