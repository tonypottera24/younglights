# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 00:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20171212_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='title',
            field=models.CharField(default='', max_length=15),
        ),
    ]
