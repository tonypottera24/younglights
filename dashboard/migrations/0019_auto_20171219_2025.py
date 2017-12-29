# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 12:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20171218_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyBachelor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toefl', models.FloatField(default=0)),
                ('sat', models.FloatField(default=0)),
                ('gpa', models.FloatField(default=0)),
                ('ielts', models.FloatField(default=0)),
                ('content', models.TextField(default='', max_length=5000)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': (('view_applymajor', 'Can view apply major'),),
            },
        ),
        migrations.CreateModel(
            name='ApplyCollege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('chinese_name', models.CharField(max_length=64)),
                ('content', models.TextField(default='', max_length=5000)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': (('view_applyschool', 'Can view apply school'),),
            },
        ),
        migrations.CreateModel(
            name='ApplyCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('chinese_name', models.CharField(max_length=64)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': (('view_applycountry', 'Can view apply country'),),
            },
        ),
        migrations.CreateModel(
            name='ApplyMajor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('chinese_name', models.CharField(max_length=64)),
                ('content', models.TextField(default='', max_length=5000)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ApplyCollege')),
            ],
            options={
                'permissions': (('view_applymajor', 'Can view apply major'),),
            },
        ),
        migrations.CreateModel(
            name='ApplyMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toefl', models.FloatField(default=0)),
                ('sat', models.FloatField(default=0)),
                ('gpa', models.FloatField(default=0)),
                ('ielts', models.FloatField(default=0)),
                ('content', models.TextField(default='', max_length=5000)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ApplyMajor')),
            ],
            options={
                'permissions': (('view_applymajor', 'Can view apply major'),),
            },
        ),
        migrations.CreateModel(
            name='ApplyPhD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toefl', models.FloatField(default=0)),
                ('sat', models.FloatField(default=0)),
                ('gpa', models.FloatField(default=0)),
                ('ielts', models.FloatField(default=0)),
                ('content', models.TextField(default='', max_length=5000)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ApplyMajor')),
            ],
            options={
                'permissions': (('view_applymajor', 'Can view apply major'),),
            },
        ),
        migrations.CreateModel(
            name='ApplySchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('chinese_name', models.CharField(max_length=64)),
                ('content', models.TextField(default='', max_length=5000)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': (('view_applyschool', 'Can view apply school'),),
            },
        ),
        migrations.CreateModel(
            name='ApplyState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('chinese_name', models.CharField(max_length=64)),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ApplyCountry')),
            ],
            options={
                'permissions': (('view_applystate', 'Can view apply state'),),
            },
        ),
        migrations.AddField(
            model_name='applyschool',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ApplyState'),
        ),
        migrations.AddField(
            model_name='applycollege',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ApplySchool'),
        ),
        migrations.AddField(
            model_name='applybachelor',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ApplyMajor'),
        ),
    ]