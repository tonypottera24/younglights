# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 20:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20171209_0412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('view_administrator', 'Can view administrator'), ('add_administrator', 'Can add administrator'), ('change_administrator', 'Can change administrator'), ('delete_administrator', 'Can delete administrator'), ('view_teacher', 'Can view teacher'), ('add_teacher', 'Can add teacher'), ('change_teacher', 'Can change teacher'), ('delete_teacher', 'Can delete teacher'), ('view_student', 'Can view student'), ('add_student', 'Can add student'), ('change_student', 'Can change student'), ('delete_student', 'Can delete student'))},
        ),
    ]
