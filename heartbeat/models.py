from __future__ import unicode_literals

from django.db import models


class MonitorAgent(models.Model):
    hostname = models.GenericIPAddressField()
    register_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.BooleanField(default=True)
    update_status = models.BooleanField(default=False)

    @property
    def uuids(self):
        return [instance_uuid.uuid for instance_uuid in self.instances_uuid.all() if self.instances_uuid.all()]

    def __unicode__(self):
        return self.hostname


class InstanceUUID(models.Model):
    uuid = models.CharField(max_length=128)
    agent = models.ForeignKey(MonitorAgent, related_name='instances_uuid')

    def __unicode__(self):
        return ''.join([self.agent.hostname, ':', self.uuid])
