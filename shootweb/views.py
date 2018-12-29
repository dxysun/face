# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from shootweb.models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect
import math
from scipy.interpolate import interp1d
import numpy as np
import json
import datetime


# Create your views here.
# 把datetime转成字符串
def time_to_string(dt):
    return dt.strftime("%H:%M:%S")


def time_to_string_mill(dt):
    return dt.strftime("%H:%M:%S.%f")


# 把字符串转成datetime
def string_to_time(string):
    return datetime.datetime.strptime(string, "%H:%M:%S")


# 把字符串转成datetime
def string_to_time_mill(string):
    return datetime.datetime.strptime(string, "%H:%M:%S.%f")


def get_max_five(x_data, y_data):
    xdata = {}
    ydata = {}
    i = 0
    for d in x_data:
        xdata[i] = d
        i += 1
    i = 0
    for y in y_data:
        ydata[i] = y
        i += 1
    x_top = sorted(xdata.items(), key=lambda x: x[1], reverse=True)
    x_top_five = dict(x_top[0:5])
    x_top_five = dict(sorted(x_top_five.items(), key=lambda x: x[0]))
    y_five = []
    for key in x_top_five.keys():
        y_five.append(ydata[key])
    return x_top_five.values(), y_five


def convert_x_y(x, y):
    if abs(x) <= 10:
        x = 0
    else:
        if x < 0:
            x = ((abs(x) - 10) / 40) * -1
        else:
            x = (x - 10) / 40
    if abs(y) <= 10:
        y = 0
    else:
        if y < 0:
            y = ((abs(y) - 10) / 40) * -1
        else:
            y = (y - 10) / 40
    return x, y


# 极坐标与直角坐标的关系：
# x=ρcos φ，y=ρsin φ
# 直角坐标与极坐标的关系：
# ρ²=x²+y²
# tan φ=y/x
def cart_to_polar(x, y):
    x, y = convert_x_y(x, y)
    z = pow(x, 2) + pow(y, 2)
    r = math.sqrt(z)
    angle = math.atan2(y, x) * 180 / math.pi
    if angle < 0:
        angle = 360 + angle
    r = round(r, 2)
    angle = round(angle, 2)
    return r, angle


def polar_to_cart(x, y, r):
    x_data = []
    y_data = []
    x_start = x + r * math.cos(0 * math.pi / 180)
    y_start = y + r * math.sin(0 * math.pi / 180)
    for angle in range(0, 360):
        x1 = x + r * math.cos(angle * math.pi / 180)
        y1 = y + r * math.sin(angle * math.pi / 180)
        x_data.append(round(x1, 2))
        y_data.append(round(y1, 2))
    x_data.append(x_start)
    y_data.append(y_start)
    return x_data, y_data


def update_data(user_name):
    shake_datas = shake_all_info.objects.filter(is_process=0).filter(user_name=user_name)
    for data in shake_datas:
        record_time = data.record_time
        # record_time = time_to_string_mill(string_to_time(record_time) - datetime.timedelta(seconds=7))
        report_times = shoot_report.objects.filter(shoot_date=data.record_date).filter(
            start_time__lte=record_time).filter(end_time__gte=record_time)
        if len(report_times) > 0:
            # print(len(report_times))
            print(data.record_time + " shake  find report data " + report_times[0].start_time)
            if string_to_time(data.end_time) - string_to_time(data.start_time) <= datetime.timedelta(seconds=2):
                print("delete " + data.record_time)
                data.delete()
        else:
            print(data.record_time + " shake  not find report data")
            data.is_process = 1
            data.delete()

    shoot_reports = shoot_report.objects.filter(is_process=0).filter(user_name=user_name)
    if len(shoot_reports) > 0:
        for report in shoot_reports:
            # report_time = time_to_string_mill(string_to_time_mill(report.shoot_time) + datetime.timedelta(seconds=10))
            # print(report_time)
            report_time = time_to_string_mill(string_to_time_mill(report.shoot_time) + datetime.timedelta(seconds=2))
            shake_times = shake_all_info.objects.filter(record_date=report.shoot_date).filter(
                start_time__lte=report_time).filter(end_time__gte=report_time)
            if len(shake_times) == 1:
                print('find shake:' + report.shoot_time)
                shake = shake_times[0]
                report.x_shake_data = shake.beside_x_data
                report.y_shake_data = shake.beside_y_data
                report.x_shake_pos = shake.beside_x_pos
                report.y_shake_pos = shake.beside_y_pos
                report.x_up_shake_data = shake.up_x_data
                report.y_up_shake_data = shake.up_y_data
                report.x_up_shake_pos = shake.up_x_pos
                report.y_up_shake_pos = shake.up_y_pos
                report.is_process = 1
                shake.is_process = 1
                shake.save()
                report.save()
            else:
                print('not find shake ' + report.shoot_time)
            grades = shoot_grade.objects.filter(report_id=report.id)
            for grade in grades:
                heart_times = heart_data.objects.filter(heart_date=grade.grade_date).filter(heart_time=grade.grade_time)
                if len(heart_times) >= 1:
                    print('find heart data')
                    heart_time = heart_times[0]
                    grade.heart_rate = heart_time.average_rate
                else:
                    print('no heart data')
                    grade.heart_rate = 0
                grade.save()


def insert(x_data, y_data):
    x = []
    for i in range(1, len(x_data) * 5, 5):
        x.append(i)
    x = np.array(x)
    x_f3 = interp1d(x, x_data, kind='cubic')
    y_f3 = interp1d(x, y_data, kind='cubic')
    x_data_new = []
    y_data_new = []
    for i in range(x.min(), x.max() + 1):
        x_data_new.append(str(round(float(x_f3(i).tolist()), 2)))
        y_data_new.append(str(round(float(y_f3(i).tolist()), 2)))
    return x_data_new, y_data_new


def get_int_data(list_data, is_negative=False):
    temp_data = []
    for data in list_data:
        d = int(data)
        if is_negative:
            d *= -1
        temp_data.append(d)
    return temp_data


def shake_data_process(data_shake, is_negative=False):
    plus_num = 0
    data_plus_array = []
    for i in range(0, len(data_shake)):
        data = float(data_shake[i])
        if is_negative:
            data *= -1
        plus_num += data
        plus_num = round(plus_num, 2)
        data_plus_array.append(plus_num)
    return data_plus_array


def shake_get_plus_shoot_point(data_plus_array, nums, is_insert=False):
    pos_array = []
    pos = []
    j = 0
    n = 10
    m = 2
    if is_insert:
        n *= 5
        m = 5
    for i in range(0, len(data_plus_array)):
        plus_num = data_plus_array[i]
        if j < len(nums) and i == nums[j]:
            if i - n > 0:
                pos_array.append(data_plus_array[i - n:i + m])
            else:
                pos_array.append(data_plus_array[0:i + m])
            pos.append(plus_num)
            j += 1
    return pos, pos_array


def cut_shake_data(y_shake_data):
    count_smooth = 0
    rank = -1
    for data in y_shake_data:
        rank += 1
        if count_smooth < 5 and 10 < int(data):
            count_smooth = 0
            continue
        if abs(data) < 10:
            # print(data)
            count_smooth += 1
        if count_smooth == 5:
            break
    # print(rank)
    return y_shake_data[rank - 4:], rank - 4


def process_grade_rapid_time(rapid_data):
    data = []
    for i in range(0, len(rapid_data)):
        if i == 0:
            data.append(float(rapid_data[i]))
        else:
            data.append(round(float(rapid_data[i]) - float(rapid_data[i - 1]), 2))
    return data


def get_shoot_point(beside_y_data, is_insert=False, limit=10):
    nums = []
    is_smooth = False
    count_smooth = 0
    for i in range(0, len(beside_y_data)):
        y = beside_y_data[i]
        if is_smooth and y > limit:
            if beside_y_data[i - 1] > 5:
                if is_insert:
                    nums.append((i - 2) * 5)
                else:
                    nums.append(i - 2)
            else:
                if is_insert:
                    nums.append((i - 1) * 5)
                else:
                    nums.append(i - 1)
            count_smooth = 0
            is_smooth = False
            continue
        if len(nums) == 5:
            break
        if y > limit:
            count_smooth = 0
        else:
            count_smooth += 1
            if count_smooth >= 5:
                is_smooth = True
    return nums


def fun(x, a, b, c):
    return a * x * x + b * x + c


def process_shake_pos_info(beside_x_pos, beside_y_pos, up_x_pos, up_y_pos):
    beside_x_pos = beside_x_pos.split(",")
    beside_y_pos = beside_y_pos.split(",")
    up_x_pos = up_x_pos.split(",")
    up_y_pos = up_y_pos.split(",")
    beside_x_data = "0,"
    beside_y_data = "0,"
    up_x_data = "0,"
    up_y_data = "0,"
    for i in range(1, len(beside_x_pos)):
        d_x = int(beside_x_pos[i]) - int(beside_x_pos[i - 1])
        d_y = int(beside_y_pos[i]) - int(beside_y_pos[i - 1])
        beside_x_data += str(d_x) + ","
        beside_y_data += str(d_y) + ","
    beside_x_data = beside_x_data[:-1]
    beside_y_data = beside_y_data[:-1]

    for i in range(1, len(up_x_pos)):
        d_x = int(up_x_pos[i]) - int(up_x_pos[i - 1])
        d_y = int(up_y_pos[i]) - int(up_y_pos[i - 1])
        up_x_data += str(d_x) + ","
        up_y_data += str(d_y) + ","
    up_x_data = up_x_data[:-1]
    up_y_data = up_y_data[:-1]
    return beside_x_data, beside_y_data, up_x_data, up_y_data


def array_to_str(data):
    data_str = ""
    for i in range(0, len(data)):
        data_str += str(data[i]) + ","
    return data_str[:-1]


def get_up_shoot_limit(x_up_shoot_pos, x_pos, grades):
    up_x_10_pos = []
    up_shake_rate = None
    if len(x_up_shoot_pos) == 5:
        if x_pos[0] > 0:
            left = 50 - x_pos[0]
        else:
            left = 50 + x_pos[0]
        if x_pos[4] > 0:
            right = 50 + x_pos[4]
        else:
            right = 50 - x_pos[4]
        pos_cha = 3100 - (left + right)
        up_x_cha = (x_up_shoot_pos[4] - x_up_shoot_pos[0]) * -1
        up_shake_rate = pos_cha / up_x_cha
        # print(up_shake_rate)
        for i in range(0, 5):
            if grades[i] == 10:
                if x_pos[i] > 0:
                    cha10_r = 50 - abs(x_pos[i])
                    cha10_r = cha10_r / up_shake_rate
                    cha10_r = x_up_shoot_pos[i] + cha10_r
                    cha10_l = 50 + abs(x_pos[i])
                    cha10_l = cha10_l / up_shake_rate
                    cha10_l = x_up_shoot_pos[i] - cha10_l
                else:
                    cha10_r = 50 + abs(x_pos[i])
                    cha10_r = cha10_r / up_shake_rate
                    cha10_r = x_up_shoot_pos[i] + cha10_r
                    cha10_l = 50 - abs(x_pos[i])
                    cha10_l = cha10_l / up_shake_rate
                    cha10_l = x_up_shoot_pos[i] - cha10_l
                up_x_10_pos.append(round(cha10_r, 2))
                up_x_10_pos.append(round(cha10_l, 2))
            if grades[i] == 9 or grades[i] == 8:
                if x_pos[i] > 0:
                    cha10_r = abs(x_pos[i]) - 50
                    cha10_r = cha10_r / up_shake_rate
                    cha10_r = x_up_shoot_pos[i] - cha10_r
                    cha10_l = abs(x_pos[i]) + 50
                    cha10_l = cha10_l / up_shake_rate
                    cha10_l = x_up_shoot_pos[i] - cha10_l
                else:
                    cha10_r = abs(x_pos[i]) + 50
                    cha10_r = cha10_r / up_shake_rate
                    cha10_r = x_up_shoot_pos[i] + cha10_r
                    cha10_l = abs(x_pos[i]) - 50
                    cha10_l = cha10_l / up_shake_rate
                    cha10_l = x_up_shoot_pos[i] + cha10_l
                up_x_10_pos.append(round(cha10_r, 2))
                up_x_10_pos.append(round(cha10_l, 2))
    return up_x_10_pos, up_shake_rate


def split_report(reports):
    temp_report = []
    all_report = []
    temp_report.append(reports[0])
    for i in range(1, len(reports)):
        # print(reports[i].start_time)
        if len(reports[i - 1].start_time) > 3:
            r1_time = string_to_time_mill(reports[i - 1].start_time)
            r2_time = string_to_time_mill(reports[i].start_time)
            # print(r1_time)
            # print(r2_time)
            if r2_time - r1_time > datetime.timedelta(minutes=5):
                all_report.append(temp_report)
                temp_report = []
            temp_report.append(reports[i])

    if len(temp_report) > 0:
        all_report.append(temp_report)
    return all_report


def get_grade_stability(x_pos, y_pos):
    res = 0
    for x, y in zip(x_pos, y_pos):
        res += math.sqrt(x * x + y * y)
    return round(res / len(x_pos), 2)


def process_pos_array(pos_array, shoot_pos, grade_pos, up_shake_rate, is_average=False):
    y_pos_average_str = []
    y_pos_str = []
    last_num = None
    temp_sum = 0
    i = 5 - len(shoot_pos)
    shoot_point = []
    for pos_a in pos_array:
        temp = []
        for y_d in pos_a:
            if is_average:
                if last_num is not None:
                    cha = y_d - last_num
                    temp_sum += cha
                last_num = y_d
            d1 = round(y_d - shoot_pos[i], 2) + int(grade_pos[i] / up_shake_rate)
            temp.append(d1)
        shoot_point.append(int(grade_pos[i] / up_shake_rate))
        i += 1
        if is_average:
            y_pos_average_str.append(round(temp_sum / (len(pos_a) - 1), 2))
        y_pos_str.append(temp)
    if is_average:
        return y_pos_str, shoot_point, y_pos_average_str
    else:
        return y_pos_str, shoot_point


def get_shoot_date(user_name):
    shoot_reports = shoot_report.objects.filter(user_name=user_name).values('shoot_date').distinct()
    shoot_dates = []
    for r in shoot_reports:
        shoot_dates.append(r['shoot_date'])
    return shoot_dates


def index(request):
    return render(request, 'main.html')


def login_admin(request):
    if request.method == 'GET':
        return render(request, 'login_admin.html')
    result = {}
    if request.method == "POST":  # 请求方法为POST时，进行处理
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = user_info.objects.filter(user_name=username)
        if len(user) == 0:
            result["status"] = "failed"
        elif user[0].password == password:
            request.session["username"] = username
            request.session["user_id"] = user[0].id
            request.session["user"] = "admin"
            request.session["role"] = "admin"
            result["status"] = "success"
        else:
            result["status"] = "failed"
        return JsonResponse(result)


def get_user_info(request):
    if request.method == 'POST':
        users = user_info.objects.filter(role="athlete")
        result = {}
        result['data'] = []
        for user in users:
            u = {}
            u['id'] = user.id
            u['user_name'] = user.user_name
            result['data'].append(u)
        if len(users) > 0:
            result["status"] = "success"
        else:
            result["status"] = "failed"
        return JsonResponse(result)


def login(request):
    if request.method == 'GET':
        users = user_info.objects.filter(role="athlete")
        return render(request, 'shoot_login.html', {
            "users": users
        })
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user = user_info.objects.get(id=int(user_id))

        request.session['user'] = user.user_name
        request.session['user_id'] = user.id
        request.session['role'] = user.role
        return redirect("sport_home")


def logout(request):
    del request.session["user"]
    del request.session["role"]
    del request.session["user_id"]
    return redirect("login")


def register(request):
    return render(request, 'register.html')


def main(request):
    return render(request, 'main.html')


def sport_home(request):
    return render(request, 'sport_home.html')


def coach_home(request):
    return render(request, 'coach_home.html')


def coach_sport_info(request):
    return render(request, 'coach_sport_info.html')


def coach_game_info(request):
    return render(request, 'coach_game_info.html')


def coach_sport_info_detail(request):
    return render(request, 'coach_sport_info_detail.html')


def sport_game_analyse(request):
    user_name = request.session.get('user', "")
    shoot_reports = []
    best_grade = 0
    bad_grade = 100
    total_grade = 0
    report_num = 0
    average_grade = 0
    quadrant = [0, 0, 0, 0]
    right_up = 0
    left_up = 0
    left_blow = 0
    right_blow = 0
    grades = []
    r_pos = []
    p_pos = []
    x_pos = []
    y_pos = []
    hearts = []
    report_shake_info = []
    if request.method == 'POST':
        report_id = request.POST['report_id']
        ids = report_id.split(",")
        for id in ids:
            # print(id)
            report_num += 1
            report = shoot_report.objects.get(id=id)
            grade = float(report.total_grade)
            grades.append(grade)
            total_grade += grade
            if grade > best_grade:
                best_grade = grade
            if grade < bad_grade:
                bad_grade = grade
            shoot_reports.append(report)

            shake_info = {}
            shoot_grades = shoot_grade.objects.filter(report_id=id)
            heart_temp = []
            heart_total = 0
            shake_info['x_pos'] = []
            shake_info['y_pos'] = []
            shake_info['grades'] = []
            for grade in shoot_grades:
                # print(grade.id)
                shake_info['grades'].append(grade.grade)
                x = float(grade.x_pos)
                y = float(grade.y_pos)
                x_pos.append(x)
                shake_info['x_pos'].append(x)
                shake_info['y_pos'].append(y)
                y_pos.append(y)
                r, p = cart_to_polar(x, y)
                r = 11 - r
                r_pos.append(r)
                p_pos.append(p)
                if x > 0 and y > 0:
                    quadrant[0] += 1
                    right_up += 1
                if x < 0 and y > 0:
                    quadrant[1] += 1
                    left_up += 1
                if x < 0 and y < 0:
                    quadrant[2] += 1
                    left_blow += 1
                if x > 0 and y < 0:
                    quadrant[3] += 1
                    right_blow += 1
                if grade.heart_rate is not None and grade.heart_rate != 0:
                    heart_temp.append(grade.heart_rate)
                    heart_total += grade.heart_rate
            if len(heart_temp) != 0:
                heart = heart_total / len(heart_temp)
            else:
                heart = 0
            hearts.append(heart)
            if report.x_shake_pos is not None and report.x_up_shake_pos is not None:
                x_shake_data, y_shake_data, x_up_shake_data, y_up_shake_data = process_shake_pos_info(
                    report.x_shake_pos,
                    report.y_shake_pos,
                    report.x_up_shake_pos,
                    report.y_up_shake_pos)
                is_insert = False
                y_data = y_shake_data.split(",")
                x_up_data = x_up_shake_data.split(",")
                y_up_data = y_up_shake_data.split(",")

                y_data = get_int_data(y_data, is_negative=True)
                x_up_data = get_int_data(x_up_data)
                y_up_data = get_int_data(y_up_data)

                y_data, num = cut_shake_data(y_data)
                x_up_data = x_up_data[num:]
                y_up_data = y_up_data[num:]

                y_data_plus = shake_data_process(y_data)
                x_up_data_plus = shake_data_process(x_up_data)

                nums = get_shoot_point(y_data, is_insert=is_insert)
                up_nums = get_shoot_point(y_up_data, is_insert=is_insert, limit=5)

                y_shoot_pos, y_pos_array = shake_get_plus_shoot_point(y_data_plus, nums, is_insert=is_insert)
                x_shoot_pos, x_pos_array = shake_get_plus_shoot_point(x_up_data_plus, nums,
                                                                      is_insert=is_insert)
                x_up_shoot_pos, _ = shake_get_plus_shoot_point(x_up_data_plus, up_nums, is_insert=is_insert)
                up_x_10_pos, up_shake_rate = get_up_shoot_limit(x_up_shoot_pos, shake_info['x_pos'],
                                                                shake_info['grades'])

                shake_info['y_data_plus'] = y_data_plus
                shake_info['x_up_data_plus'] = x_up_data_plus
                shake_info['x_shoot_pos'] = x_shoot_pos
                shake_info['y_shoot_pos'] = y_shoot_pos
                shake_info['up_shake_rate'] = up_shake_rate
            report_shake_info.append(shake_info)
        average_grade = round(total_grade / report_num, 2)
    # average_in_circle = shootlib.get_average_in_circle(x_pos, y_pos)
    # print(average_in_circle)
    grade_stability = get_grade_stability(x_pos, y_pos)
    grade_info = dict(grades=grades, r_pos=r_pos, p_pos=p_pos, hearts=hearts, grade_stability=grade_stability)
    return render(request, 'sport_game_analyse.html', {
        'shoot_reports': shoot_reports,
        'grade_info': json.dumps(grade_info),
        'report_shake_info': json.dumps(report_shake_info),
        'best_grade': best_grade,
        'bad_grade': bad_grade,
        'average_grade': average_grade,
        'right_up': right_up,
        'left_up': left_up,
        'left_blow': left_blow,
        'right_blow': right_blow,
    })


def sport_game_analyse_id(request):
    report_id = request.GET['id']
    report = shoot_report.objects.get(id=report_id)
    grades = []
    hearts = []
    r_pos = []
    p_pos = []
    x_pos = []
    y_pos = []
    shoot_grades = shoot_grade.objects.filter(report_id=report_id).order_by('grade_detail_time')
    rapid_data = []
    for grade in shoot_grades:
        rapid_data.append(grade.rapid_time)
        grades.append(float(grade.grade))
        x_pos.append(float(grade.x_pos))
        y_pos.append(float(grade.y_pos))
        x = float(grade.x_pos)
        y = float(grade.y_pos)
        r, p = cart_to_polar(x, y)
        r = 11 - r
        r_pos.append(r)
        p_pos.append(p)
        hearts.append(grade.heart_rate)
    grade_stability = get_grade_stability(x_pos, y_pos)
    grade_info = dict(r_pos=r_pos, p_pos=p_pos, x_pos=x_pos, y_pos=y_pos, grades=grades, hearts=hearts,
                      grade_stability=grade_stability)

    shake_info = {}
    five_pos_info = {}
    x_data_pos = report.x_shake_pos
    y_data_pos = report.y_shake_pos
    x_up_data_pos = report.x_up_shake_pos
    y_up_data_pos = report.y_up_shake_pos

    nums = []
    if report.x_shake_pos is not None and report.x_up_shake_pos is not None:
        x_shake_data, y_shake_data, x_up_shake_data, y_up_shake_data = process_shake_pos_info(
            report.x_shake_pos,
            report.y_shake_pos,
            report.x_up_shake_pos,
            report.y_up_shake_pos)
        is_insert = True
        x_data = x_shake_data.split(",")
        y_data = y_shake_data.split(",")
        x_up_data = x_up_shake_data.split(",")
        y_up_data = y_up_shake_data.split(",")

        x_data_pos = x_data_pos.split(",")
        y_data_pos = y_data_pos.split(",")
        x_up_data_pos = x_up_data_pos.split(",")
        y_up_data_pos = y_up_data_pos.split(",")

        x_data = get_int_data(x_data)
        y_data = get_int_data(y_data, is_negative=True)
        x_up_data = get_int_data(x_up_data)
        y_up_data = get_int_data(y_up_data)

        x_data_pos = get_int_data(x_data_pos)
        y_data_pos = get_int_data(y_data_pos)
        x_up_data_pos = get_int_data(x_up_data_pos)
        y_up_data_pos = get_int_data(y_up_data_pos)

        y_data, num = cut_shake_data(y_data)
        x_data = x_data[num:]
        x_up_data = x_up_data[num:]
        y_up_data = y_up_data[num:]

        x_data_pos = x_data_pos[num:]
        y_data_pos = y_data_pos[num:]
        x_up_data_pos = x_up_data_pos[num:]
        y_up_data_pos = y_up_data_pos[num:]

        nums = get_shoot_point(y_data, is_insert=is_insert)
        up_nums = get_shoot_point(y_up_data, is_insert=is_insert, limit=5)
        # print(nums)
        # print(up_nums)

        if is_insert:
            x_data, y_data = insert(x_data, y_data)
            x_up_data, y_up_data = insert(x_up_data, y_up_data)

        x_data_plus = shake_data_process(x_data)
        y_data_plus = shake_data_process(y_data)
        x_up_data_plus = shake_data_process(x_up_data)
        y_up_data_plus = shake_data_process(y_up_data, is_negative=True)

        y_shoot_pos, y_pos_array = shake_get_plus_shoot_point(y_data_plus, nums, is_insert=is_insert)
        x_shoot_pos, x_pos_array = shake_get_plus_shoot_point(x_up_data_plus, nums, is_insert=is_insert)

        x_up_shoot_pos, _ = shake_get_plus_shoot_point(x_up_data_plus, up_nums, is_insert=is_insert)
        y_up_shoot_pos, _ = shake_get_plus_shoot_point(y_up_data_plus, up_nums, is_insert=is_insert)

        up_x_10_pos, up_shake_rate = get_up_shoot_limit(x_up_shoot_pos, x_pos, grades)
        # print(x_up_shoot_pos)
        # print(up_x_10_pos)
        if up_shake_rate is not None:
            x_pos_str, x_shoot_point = process_pos_array(x_pos_array, x_shoot_pos, x_pos, up_shake_rate)
            y_pos_str, y_shoot_point, y_pos_average_str = process_pos_array(y_pos_array, y_shoot_pos, y_pos,
                                                                            up_shake_rate, is_average=True)
            five_pos_info['up_shake_rate'] = up_shake_rate
            five_pos_info['x_pos_str'] = x_pos_str
            five_pos_info['y_pos_str'] = y_pos_str
            five_pos_info['y_pos_average_str'] = y_pos_average_str
            five_pos_info['x_shoot_point'] = x_shoot_point
            five_pos_info['y_shoot_point'] = y_shoot_point

        shake_info['x_data_plus'] = x_data_plus
        shake_info['y_data_plus'] = y_data_plus
        shake_info['x_data_ori'] = x_data
        shake_info['y_data_ori'] = y_data

        shake_info['x_up_data_plus'] = x_up_data_plus
        shake_info['x_up_data_ori'] = x_up_data
        shake_info['y_up_data_plus'] = y_up_data_plus
        shake_info['y_up_data_ori'] = y_up_data

        shake_info['x_data_pos'] = x_data_pos
        shake_info['y_data_pos'] = y_data_pos
        shake_info['x_up_data_pos'] = x_up_data_pos
        shake_info['y_up_data_pos'] = y_up_data_pos

        shake_info['y_shoot_pos'] = y_shoot_pos
        shake_info['x_shoot_pos'] = x_shoot_pos
        shake_info['x_up_shoot_pos'] = x_up_shoot_pos
        shake_info['y_up_shoot_pos'] = y_up_shoot_pos
        shake_info['up_x_10_pos'] = up_x_10_pos

    nums = array_to_str(nums)
    return render(request, 'sport_game_analyse_id.html', {
        'shoot_reports': report,
        'grade_info': json.dumps(grade_info),
        'shake_info': json.dumps(shake_info),
        'five_pos_info': json.dumps(five_pos_info),
        'shoot_info': shoot_grades,
        'beside_y_nums': nums,
    })


def sport_game_history(request):
    user_name = request.session.get('user', "")
    # update_data(user_name)
    shoot_dates = get_shoot_date(user_name)
    if request.method == 'GET':
        report = shoot_report.objects.filter(user_name=user_name).last()
        shoot_reports = None
        date = None
        all_report = None
        if report is not None:
            date = report.shoot_date
            shoot_reports = shoot_report.objects.filter(shoot_date=report.shoot_date).filter(
                user_name=user_name).order_by('shoot_time')
            # print(len(shoot_reports))
            all_report = split_report(shoot_reports)
        return render(request, 'sport_game_history.html', {
            'shoot_reports': shoot_reports,
            'all_report': all_report,
            'shoot_dates': shoot_dates,
            'date1': date,
            'date2': date
        })
    else:
        date1 = request.POST['date1']
        date2 = request.POST['date2']
        # shoot_reports = shoot_report.objects.filter(user_name=user_name).filter(shoot_date__gte=date1).filter(
        #     shoot_date__lte=date2).order_by('shoot_time').order_by('shoot_date')
        shoot_reports = shoot_report.objects.filter(user_name=user_name).filter(shoot_date=date1).order_by('shoot_time')
        all_report = split_report(shoot_reports)
        return render(request, 'sport_game_history.html', {
            'shoot_reports': shoot_reports,
            'all_report': all_report,
            'shoot_dates': shoot_dates,
            'date1': date1,
            'date2': date2
        })


def admin_home(request):
    if request.method == 'POST':
        item_name = request.POST['item_name']
        item_intro = request.POST['item_intro']
        item_rule = request.POST['item_rule']
        print(item_name)
        shoot_item = shoot_items(item_name=item_name, item_info=item_intro, item_rule=item_rule)
        shoot_item.save()
    items = shoot_items.objects.all()
    all_item = []
    for item in items:
        info = {}
        info["id"] = item.id
        info["item_name"] = item.item_name
        coachs = user_info.objects.filter(item_id=item.id).filter(role="coach")
        athletes = user_info.objects.filter(item_id=item.id).filter(role="athlete")
        coach_str = ""
        for coach in coachs:
            coach_str += coach.user_name + ","
        info["coach"] = coach_str[:-1]
        info["athlete_num"] = len(athletes)
        all_item.append(info)
    return render(request, 'admin_home.html', {
        "shoot_items": all_item
    })


def admin_coach(request):
    if request.method == 'POST':
        coach_name = request.POST['coach_name']
        gender = request.POST['gender']
        age = request.POST['age']
        coach_info = request.POST['coach_info']
        item_id = request.POST['item_id']
        password = request.POST['password']
        print(coach_name)
        coach = user_info(user_name=coach_name, gender=gender, age=age, intro=coach_info, item_id=item_id,
                          password=password, role="coach")
        coach.save()
    coachs = user_info.objects.filter(role="coach")
    all_cocahs = []
    for coach in coachs:
        c = {}
        items = shoot_items.objects.filter(id=coach.item_id)
        c["coach"] = coach
        if len(items) > 0:
            item = items[0]
            c["item_name"] = item.item_name
        else:
            c["item_name"] = ""
        all_cocahs.append(c)
    return render(request, 'admin_coach.html', {
        "coachs": all_cocahs
    })


def admin_sport(request):
    if request.method == 'POST':
        athlete_name = request.POST['athlete_name']
        gender = request.POST['gender']
        age = request.POST['age']
        athlete_info = request.POST['athlete_info']
        item_id = request.POST['item_id']
        password = request.POST['password']
        print(athlete_name)
        athlete = user_info(user_name=athlete_name, gender=gender, age=age, intro=athlete_info, item_id=item_id,
                            password=password, role="athlete")
        athlete.save()
    user_infos = user_info.objects.filter(role="athlete")
    all_athletes = []
    for athlete in user_infos:
        c = {}
        items = shoot_items.objects.filter(id=athlete.item_id)
        c["athlete"] = athlete
        if len(items) > 0:
            item = items[0]
            c["item_name"] = item.item_name
        else:
            c["item_name"] = ""
        all_athletes.append(c)
    return render(request, 'admin_sport.html', {
        'athletes': all_athletes
    })


def admin_analyse(request):
    return render(request, 'admin_analyse.html')


def admin_add_item(request):
    return render(request, 'admin_add_item.html')


def admin_delete_item(request):
    if request.method == 'GET':
        id = request.GET['id']
        users = user_info.objects.filter(item_id=int(id))
        if len(users) > 0:
            for user in users:
                user.item_id = None
                user.save()
        shoot_items.objects.get(id=id).delete()
    return redirect("admin_home")


def admin_modify_item(request):
    if request.method == 'GET':
        id = request.GET['id']
        shoot_item = shoot_items.objects.get(id=int(id))
        return render(request, 'admin_modify_item.html', {
            'shoot_item': shoot_item
        })
    if request.method == 'POST':
        id = request.POST['id']
        shoot_item = shoot_items.objects.get(id=int(id))
        shoot_item.item_name = request.POST['item_name']
        shoot_item.item_info = request.POST['item_info']
        shoot_item.item_rule = request.POST['item_rule']
        shoot_item.save()
        return redirect("admin_home")


def admin_add_coach(request):
    items = shoot_items.objects.all()
    return render(request, 'admin_add_coach.html', {
        "items": items
    })


def admin_delete_coach(request):
    if request.method == 'GET':
        id = request.GET['id']
        user_info.objects.get(id=id).delete()
    return redirect("admin_coach")


def admin_modify_coach(request):
    if request.method == 'GET':
        id = request.GET['id']
        coach = user_info.objects.get(id=int(id))
        items = shoot_items.objects.all()
        return render(request, 'admin_modify_coach.html', {
            'coach': coach,
            'items': items
        })
    if request.method == 'POST':
        id = request.POST['id']
        coach = user_info.objects.get(id=int(id))
        coach.user_name = request.POST['coach_name']
        coach.intro = request.POST['coach_info']
        coach.gender = request.POST['gender']
        coach.age = request.POST['age']
        coach.item_id = request.POST['item_id']
        coach.password = request.POST['password']
        coach.save()
        return redirect("admin_coach")


def admin_add_sport(request):
    items = shoot_items.objects.all()
    return render(request, 'admin_add_sport.html', {
        "items": items
    })


def admin_delete_sport(request):
    if request.method == 'GET':
        id = request.GET['id']
        user_info.objects.get(id=id).delete()
    return redirect("admin_sport")


def admin_modify_sport(request):
    if request.method == 'GET':
        id = request.GET['id']
        athlete = user_info.objects.get(id=int(id))
        items = shoot_items.objects.all()
        return render(request, 'admin_modify_sport.html', {
            'athlete': athlete,
            'items': items
        })
    if request.method == 'POST':
        id = request.POST['id']
        athlete = user_info.objects.get(id=int(id))
        athlete.user_name = request.POST['user_name']
        athlete.intro = request.POST['athlete_info']
        athlete.gender = request.POST['gender']
        athlete.age = request.POST['age']
        athlete.item_id = None
        if request.POST['item_id'] is not None:
            athlete.item_id = request.POST['item_id']
        athlete.password = request.POST['password']
        athlete.save()
        return redirect("admin_sport")


def test(request):
    return render(request, 'test.html')


def coach(request):
    return render(request, 'coach.html')


def vue(request):
    return render(request, 'vue.html', {
        'message1': 'django'
    })
