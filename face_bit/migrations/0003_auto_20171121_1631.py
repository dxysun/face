# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-21 08:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('face_bit', '0002_auto_20171121_1537'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='faceinfo',
            new_name='face_info',
        ),
    ]