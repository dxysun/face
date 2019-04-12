# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone


class user_info(models.Model):
    user_name = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, default="")
    gender = models.CharField(max_length=10, null=True)  # 男/女
    age = models.IntegerField(null=True)
    role = models.CharField(max_length=100)  # admin, athlete, coach
    intro = models.TextField(null=True)
    item_id = models.IntegerField(null=True)
    remark = models.TextField(null=True)


class shoot_items(models.Model):
    item_name = models.CharField(max_length=100, default="")
    item_info = models.TextField(null=True)
    item_rule = models.TextField(null=True)
    remark = models.TextField(null=True)


# 记录侧面每次抖动开始和结束的时间，抖动详细信息
class record_shake_time(models.Model):
    record_date = models.CharField(max_length=200)
    record_time = models.CharField(max_length=200, default="")
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    shake_x_data = models.TextField(null=True)
    shake_x_detail_data = models.TextField(null=True)
    shake_y_data = models.TextField(null=True)
    shake_y_detail_data = models.TextField(null=True)
    is_process = models.IntegerField(default=0)
    user_name = models.CharField(max_length=100, default="")
    remark = models.TextField(null=True)


# 记录水平每次抖动开始和结束的时间，抖动详细信息
class record_up_shake_time(models.Model):
    record_date = models.CharField(max_length=200)
    record_time = models.CharField(max_length=200, default="")
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    shake_x_data = models.TextField(null=True)
    shake_x_detail_data = models.TextField(null=True)
    shake_y_data = models.TextField(null=True)
    shake_y_detail_data = models.TextField(null=True)
    is_process = models.IntegerField(default=0)
    user_name = models.CharField(max_length=100, default="")
    remark = models.TextField(null=True)


class shake_all_info(models.Model):
    record_date = models.CharField(max_length=200, default="")
    record_time = models.CharField(max_length=200, default="")
    start_time = models.CharField(max_length=200, default="")
    end_time = models.CharField(max_length=200, default="")
    beside_x_data = models.TextField(null=True)
    beside_x_pos = models.TextField(null=True)
    beside_y_data = models.TextField(null=True)
    beside_y_pos = models.TextField(null=True)
    up_x_data = models.TextField(null=True)
    up_x_pos = models.TextField(null=True)
    up_y_data = models.TextField(null=True)
    up_y_pos = models.TextField(null=True)
    is_process = models.IntegerField(default=0)
    user_name = models.CharField(max_length=100, default="")
    remark = models.TextField(null=True)


# 抖动数据
class shake_data(models.Model):
    report_id = models.IntegerField(default=0)
    record_id = models.IntegerField(default=0)
    shake_date = models.CharField(max_length=200)
    shake_time = models.CharField(max_length=200, default="")
    x_data = models.TextField(null=True)
    y_data = models.TextField(null=True)
    user_name = models.CharField(max_length=100, default="")
    remark = models.TextField(null=True)


# 记录每次心率开始和结束的时间
class record_heart_time(models.Model):
    record_date = models.CharField(max_length=200)
    record_time = models.CharField(max_length=200, default="")
    start_time = models.CharField(max_length=200, default='')
    end_time = models.CharField(max_length=200, default='')
    is_process = models.IntegerField(default=0)
    user_name = models.CharField(max_length=100, default="")
    remark = models.TextField(null=True)


# 心率数据
class heart_data(models.Model):
    report_id = models.IntegerField(default=0)
    record_id = models.IntegerField(default=0)
    heart_time = models.CharField(max_length=200)
    heart_date = models.CharField(max_length=200)
    heart_rate = models.CharField(max_length=200)
    average_rate = models.IntegerField(default=0)
    user_name = models.CharField(max_length=100, default="")
    remark = models.TextField(null=True)


# 射击成绩
class shoot_grade(models.Model):
    report_id = models.IntegerField()
    grade_date = models.CharField(max_length=200)
    grade_time = models.CharField(max_length=200)
    grade_detail_time = models.CharField(max_length=200, default="")
    grade = models.CharField(max_length=200)
    rapid_time = models.CharField(max_length=200)
    x_pos = models.CharField(max_length=200)
    y_pos = models.CharField(max_length=200)
    x_shake = models.FloatField(null=True)
    y_shake = models.FloatField(null=True)
    heart_rate = models.IntegerField(null=True)
    user_name = models.CharField(max_length=100, default="")
    remark = models.TextField(null=True)


# 每五次射击的开始时间和结束时间
class shoot_report(models.Model):
    shoot_date = models.CharField(max_length=200)
    shoot_time = models.CharField(max_length=200, default="")
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    total_grade = models.FloatField(null=True)
    x_shake_data = models.TextField(null=True)
    y_shake_data = models.TextField(null=True)
    x_shake_pos = models.TextField(null=True)
    y_shake_pos = models.TextField(null=True)
    x_up_shake_data = models.TextField(null=True)
    y_up_shake_data = models.TextField(null=True)
    x_up_shake_pos = models.TextField(null=True)
    y_up_shake_pos = models.TextField(null=True)
    is_process = models.IntegerField(default=0)
    user_name = models.CharField(max_length=100, default="")
    remark = models.TextField(null=True)


# 用于存储建立好的模型
class user_model_info(models.Model):
    user_name = models.CharField(max_length=100, default="")
    model_path = models.CharField(max_length=500, default="")
    build_time = models.CharField(max_length=200, default="")  # 模型建立时间
    model_type = models.IntegerField(default=0)  # 模型类型
    model_info = models.TextField(null=True)  # 模型的一些相关信息
    remark = models.TextField(null=True)
