# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 07:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trigger', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='name',
            new_name='item_name',
        ),
        migrations.AlterField(
            model_name='trigger',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='triggers', to='trigger.Item'),
        ),
    ]
