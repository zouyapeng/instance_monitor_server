#!/usr/bin/env python
# -*- coding: utf8 -*-
from contact.models import Contact
from rest_framework import serializers


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('step_user', 'id', 'username', 'tel', 'tel_status', 'email', 'email_status')