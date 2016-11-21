from django.contrib import admin

from heartbeat.models import InstanceUUID, MonitorAgent
# Register your models here.


admin.site.register(InstanceUUID)
admin.site.register(MonitorAgent)
