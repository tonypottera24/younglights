# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 07:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0042_remove_applydegree_apply_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applydegree',
            old_name='apply_course',
            new_name='apply_curriculum',
        ),
    ]