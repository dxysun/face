# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class face_info(models.Model):
    username = models.CharField(max_length=100, default="")
    filename = models.TextField()
    face_token = models.TextField()
    face_rectangle = models.TextField()
    remark = models.TextField()


class user_info(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    img_url = models.TextField()
    faceset_token = models.TextField(default="")
    face_token = models.TextField(default="")
    remark = models.TextField(default="")


class image_info(models.Model):
    img_url = models.TextField(default="")
    username = models.CharField(max_length=100)
    img_type = models.IntegerField(default=0)  # 0-未标记 1-已标记 2-已识别
    img_label = models.CharField(max_length=100, default="")  # 标记信息
    face_token = models.TextField(default="")
    remark = models.TextField(default="")     # 识别结果


class game_info(models.Model):
    username = models.CharField(max_length=100)
    score = models.IntegerField()
    date_score = models.CharField(max_length=200)
    remark = models.TextField(default="")
