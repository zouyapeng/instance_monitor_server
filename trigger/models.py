from __future__ import unicode_literals

from django.db import models
from contact.models import Contact
from heartbeat.models import InstanceUUID


class Trigger(models.Model):
    ITEM = ({
        ('cpu usage', 'cpu usage'),
        ('memory usage', 'memory usage'),
        ('disk read speed', 'disk read speed'),
        ('disk write speed', 'disk write speed'),
        ('incoming network traffic', 'incoming network traffic'),
        ('outgoing network traffic', 'outgoing network traffic')
    })

    METHOD =({
        ('max', 'max'),
        ('min', 'min'),
        ('avg', 'avg'),
    })

    METHOD_OPTION = ({
        ('>', '>'),
        ('>=', '>='),
        ('<', '<'),
        ('<=', '<='),
        ('==', '=='),
        ('!=', '!=')
    })

    step_user = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    instance_uuid = models.CharField(max_length=128)
    item = models.CharField(max_length=32, choices=ITEM)
    item_option = models.CharField(max_length=16, blank=True, null=True)
    period = models.IntegerField()
    method = models.CharField(max_length=3, choices=METHOD, default='avg')
    method_option = models.CharField(max_length=2, choices=METHOD_OPTION, default='>=')
    threshold = models.IntegerField()
    contacts = models.ManyToManyField(Contact, blank=True, related_name='trigger')
    status = models.BooleanField(default=False)

    def format_dict(self):
        return {'id': self.id,
                'name': self.name,
                'instance_uuid': self.instance_uuid,
                'item': self.item,
                'item_option': self.item_option,
                'period': self.period,
                'method': self.method,
                'method_option': self.method_option,
                'threshold': self.threshold,
                'contacts': self.contact_ids,
                'status': self.status}

    def get_events(self):
        message = ' '.join(str(val) for val in [self.item, self.period, 'minutes', self.method, self.method_option, self.threshold])
        return [{'instance': self.instance_uuid,
                 'message': message,
                 'create_time': event.create_time,
                 'end_time': event.end_time,
                 'status': event.status}
                for event in self.events.all()]

    def get_last_problem_events(self, datetime):
        message = ' '.join([self.item, self.period, self.method, self.method_option, self.threshold])
        return [{'instance': self.instance_uuid, 'message': message, 'create_time': event.create_time}
                for event in self.events.all() if event.status is True and event.create_time >= datetime]

    def get_last_all_events(self, datetime):
        message = ' '.join([self.item, self.period, self.method, self.method_option, self.threshold])
        return [{'instance': self.instance_uuid, 'message': message, 'create_time': event.create_time}
                for event in self.events.all() if event.create_time >= datetime]

    def delete(self, using=None, keep_parents=False):
        super(Trigger, self).delete(using)
        instance_uuid = InstanceUUID.objects.get(uuid=self.instance_uuid)
        instance_uuid.agent.update_status = True
        instance_uuid.agent.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Trigger, self).save(force_insert, force_update, using, update_fields)
        instance_uuid = InstanceUUID.objects.get(uuid=self.instance_uuid)
        instance_uuid.agent.update_status = True
        instance_uuid.agent.save()

    @property
    def contact_ids(self):
        return [contact.id for contact in self.contacts.all()]

    @property
    def contact_list(self):
        return [{'id': contact.id,
                 'contact': contact.username,
                 'tel': contact.tel,
                 'tel_status': contact.tel_status,
                 'email': contact.email,
                 'email_status': contact.email_status} for contact in self.contacts.all()]

    def __unicode__(self):
        return self.name


class Event(models.Model):
    EVENT_STATUS = ({
        (True, True),
        (False, False),
    })
    trigger = models.ForeignKey(Trigger, related_name='events')
    status = models.BooleanField(choices=EVENT_STATUS)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "{} - {} - {}".format(self.create_time, self.trigger.name, self.status)


