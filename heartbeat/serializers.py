from heartbeat.models import MonitorAgent
from rest_framework import serializers


class MonitorAgentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonitorAgent
        fields = ('id', 'hostname', 'register_time', 'update_time', 'uuids', 'status')

