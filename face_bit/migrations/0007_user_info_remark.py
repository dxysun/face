# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-22 02:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_bit', '0006_user_info_face_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='remark',
            field=models.TextField(default=''),
        ),
    ]
