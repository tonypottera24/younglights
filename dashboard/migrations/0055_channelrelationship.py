# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-09 15:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0054_auto_20180609_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChannelRelationship_channel', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChannelRelationship_student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_channelrelationship', 'Can view channel relationship'),),
            },
        ),
    ]