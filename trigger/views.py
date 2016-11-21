
from trigger.models import Trigger
from trigger.serializers import TriggerSerializer
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import pprint


class TriggerListCreateView(generics.ListCreateAPIView):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer

    def get(self, request, *args, **kwargs):
        triggers = super(TriggerListCreateView, self).get(request, args, kwargs)

        return triggers

    def post(self, request, *args, **kwargs):
        print self.get_serializer(data=request.data)
        return super(TriggerListCreateView, self).post(request, args, kwargs)


class TriggerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer

    def put(self, request, *args, **kwargs):
        trigger = self.get_object()
        agent = trigger.instance_uuid.agent
        agent.status = 2
        agent.save()
        return super(TriggerRetrieveUpdateDestroyView, self).put(request, args, kwargs)


class EventListView(generics.CreateAPIView):
    queryset = []

    def post(self, request, *args, **kwargs):
        events = []
        uuids = request.data.get['uuids']
        for uuid in uuids:
            events.extend(Trigger.objects.get(instance_uuid=uuid).get_problem_events())

        return Response({'events': events})