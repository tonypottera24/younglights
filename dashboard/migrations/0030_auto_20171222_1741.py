# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-22 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_auto_20171222_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyGRESubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('chinese_name', models.CharField(max_length=64)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='applydegree',
            name='gre_subject',
        ),
        migrations.AddField(
            model_name='applydegree',
            name='gre_subject',
            field=models.ManyToManyField(to='dashboard.ApplyGRESubject'),
        ),
    ]
