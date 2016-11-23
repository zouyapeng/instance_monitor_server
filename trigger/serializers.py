from trigger.models import Trigger, Event
from rest_framework import serializers


class TriggerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trigger
        fields = ('id', 'name', 'instance_uuid', 'item', 'period', 'method', 'method_option', 'threshold', 'status', 'contacts')
