#!/usr/bin/env python
# -*- coding: utf8 -*-

from celery.task import task
import smtplib
from email.mime.text import MIMEText
import datetime


@task()
def send_sms(event):
    trigger = event.trigger
    tel_list = [contact['tel'] for contact in trigger.contact_list if contact['tel_status']]

    if not tel_list:
        return

    message = ' '.join(str(val) for val in [trigger.item, trigger.period, 'minutes', trigger.method,
                                            trigger.method_option, trigger.threshold])

    time = event.create_time
    print(tel_list)
    print(message)


@task()
def send_email(event):
    trigger = event.trigger
    email_list = [contact['email'] for contact in trigger.contact_list if contact['email_status']]

    if not email_list:
        return

    subject = ' '.join(str(val) for val in [trigger.item, trigger.period, 'minutes', trigger.method,
                                            trigger.method_option, trigger.threshold])

    message = ''
    # time = event.create_time

    me = 'monitor@newtouch.com'
    msg = MIMEText(message, _subtype='plain', _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ";".join(email_list)
    try:
        server = smtplib.SMTP_SSL()
        server.connect("mail.newtouch.com", 465)
        server.login("monitor@newtouch.com", "newtouchmonitor")
        server.sendmail(me, email_list, msg.as_string())
        server.close()
    except Exception as error:
        pass
