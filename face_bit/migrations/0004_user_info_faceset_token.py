# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-21 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_bit', '0003_auto_20171121_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='faceset_token',
            field=models.TextField(default=''),
        ),
    ]
