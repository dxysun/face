# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-07 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='faceinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=100)),
                ('face_token', models.TextField()),
                ('face_rectangle', models.TextField()),
                ('remark', models.TextField()),
            ],
        ),
    ]
