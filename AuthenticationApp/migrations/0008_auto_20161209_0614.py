# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0007_auto_20161208_0634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='bookmarks',
            field=models.ManyToManyField(to='AuthenticationApp.Bookmark'),
        ),
    ]
