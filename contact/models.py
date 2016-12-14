from __future__ import unicode_literals

from django.db import models


class Contact(models.Model):
    step_user = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    action_time = models.CharField(max_length=32, blank=True, null=True)
    tel = models.CharField(max_length=32)
    tel_status = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    email_status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.username
