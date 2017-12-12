# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 06:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MentoringRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_record', models.TextField(max_length=1000)),
                ('student_record', models.TextField(max_length=1000)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('mentoring_date', models.DateField(verbose_name='mentoring date')),
                ('mentoring_time', models.TimeField(verbose_name='mentoring time')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MentoringRecord_student', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MentoringRecord_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_mentoring_record', 'Can view mentoring record'),),
            },
        ),
        migrations.CreateModel(
            name='MentoringRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(max_length=1000)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MentoringRelationship_student', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MentoringRelationship_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_mentoring_relationship', 'Can view mentoring relationship'),),
            },
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('end_datetime', models.DateTimeField(verbose_name='mentoring datetime end')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Mission_student', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Mission_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_mission', 'Can view mission'),),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chinese_name', models.CharField(default='', max_length=128)),
                ('school', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('college', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('major', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('qq', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('wechat', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('research_field', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('research_experience', models.TextField(blank=True, default='', max_length=10000, null=True)),
                ('thesis_experience', models.TextField(blank=True, default='', max_length=10000, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_administrator', 'Can view administrator'), ('view_teacher', 'Can view teacher'), ('view_student', 'Can view student')),
            },
        ),
    ]