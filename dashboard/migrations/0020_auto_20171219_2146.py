# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 13:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_auto_20171219_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applybachelor',
            options={'permissions': (('view_applybachelor', 'Can view apply bachelor'),)},
        ),
        migrations.AlterModelOptions(
            name='applymaster',
            options={'permissions': (('view_applymaster', 'Can view apply master'),)},
        ),
        migrations.AlterModelOptions(
            name='applyphd',
            options={'permissions': (('view_applyphd', 'Can view apply phd'),)},
        ),
    ]
