# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 06:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0006_auto_20161208_0552'),
    ]

    operations = [
       # migrations.RemoveField(
       #     model_name='student',
       #     name='user',
       # ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
