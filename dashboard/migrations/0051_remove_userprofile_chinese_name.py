# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-03 14:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0050_auto_20171230_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='chinese_name',
        ),
    ]
