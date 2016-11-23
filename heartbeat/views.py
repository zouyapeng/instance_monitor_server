from django.shortcuts import render
from heartbeat.models import MonitorAgent, InstanceUUID
from trigger.models import Trigger
from heartbeat.serializers import MonitorAgentSerializer
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import datetime


def get_config(agent):
    uuids = agent.instances_uuid.all()

    config = {}
    for uuid in uuids:
        config[uuid.uuid] = [trigger.format_dict() for trigger in uuid.trigger.all()]

    return config


class MonitorAgentCreateView(generics.ListCreateAPIView):
    queryset = MonitorAgent.objects.all()
    serializer_class = MonitorAgentSerializer

    def post(self, request, *args, **kwargs):
        agent_id = request.data.get('id', None)
        hostname = request.data.get('hostname', None)
        uuids = request.data.get('uuids', None)

        if agent_id and uuids is not None:
            config = None
            agent = MonitorAgent.objects.get(id=agent_id)
            if agent.update_status:
                config = get_config(agent)
                agent.update_status = False
            agent.status = True
            agent.save()

            instances_uuid = agent.instances_uuid.all()
            instances_uuid_list = [instance_uuid.uuid for instance_uuid in instances_uuid]
            for instance_uuid in instances_uuid:
                if instance_uuid.uuid not in uuids:
                    instance_uuid.delete()

            for uuid in uuids:
                if uuid not in instances_uuid_list:
                    instance_uuid = InstanceUUID(uuid=uuid, agent=agent)
                    instance_uuid.save()

            return Response({'id': agent_id, 'config': config})
        elif agent_id and uuids is None:
            config = None
            agent = MonitorAgent.objects.get(id=agent_id)
            if agent.update_status:
                config = get_config(agent)
                agent.update_status = False
            agent.status = True
            agent.update_time = datetime.datetime.now()
            agent.save()

            return Response({'id': agent_id, 'config': config})
        elif not agent_id and hostname:
            try:
                agent = MonitorAgent.objects.get(hostname=hostname)
            except MonitorAgent.DoesNotExist:
                agent = MonitorAgent(hostname=hostname, status=0)
                agent.save()

            if uuids is not None:
                instances_uuid = agent.instances_uuid.all()
                for instance_uuid in instances_uuid:
                    if instance_uuid.uuid not in uuids:
                        instance_uuid.delete()

                for uuid in uuids:
                    try:
                        InstanceUUID.objects.get(uuid=uuid)
                    except InstanceUUID.DoesNotExist:
                        instance_uuid = InstanceUUID(uuid=uuid, agent=agent)
                        instance_uuid.save()

            config = get_config(agent)
            agent.update_status = False
            agent.status = True
            agent.save()

            return Response({'id': agent.id, 'config': config})

        else:
            return Response({'id': None, 'config': None})


class InstanceUUIDRetrieveView(generics.RetrieveAPIView):
    queryset = InstanceUUID.objects.all()


