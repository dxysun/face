# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from shootweb.models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect
import math
from scipy.interpolate import interp1d
import numpy as np


# Create your views here.
def get_shoot_point(beside_y_data, is_insert=False):
    nums = []
    is_smooth = False
    count_smooth = 0
    for i in range(0, len(beside_y_data)):
        y = beside_y_data[i]
        if y > 10:
            count_smooth = 0
        else:
            count_smooth += 1
            if count_smooth > 10:
                is_smooth = True
        if is_smooth and y >= 10:
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
    return nums


def get_int_data(list_data, is_negative=False):
    temp_data = []
    for data in list_data:
        d = int(data)
        if is_negative:
            d *= -1
        temp_data.append(d)
    return temp_data


def shake_data_process(data_shake, nums=None):
    plus_num = 0
    data_ori = ""
    data_plus = ""
    data_plus_array = []
    pos_array = []
    pos = ""
    j = 0
    for i in range(0, len(data_shake)):
        data_ori += str(data_shake[i]) + ","
        data = float(data_shake[i])
        plus_num += data
        plus_num = round(plus_num, 2)
        data_plus_array.append(plus_num)
        if nums is not None:
            if j < len(nums) and i == nums[j]:
                pos_array.append(data_plus_array[i - 80:i + 1])
                pos += str(plus_num) + ","
                j += 1
        data_plus += str(plus_num) + ","
    if nums is None:
        return data_ori, data_plus
    else:
        return data_ori, data_plus, pos[:-1], pos_array


def cut_shake_data(y_shake_data):
    count_smooth = 0
    rank = -1
    for data in y_shake_data:
        rank += 1
        if count_smooth < 10 < int(data):
            count_smooth = 0
            continue
        if abs(data) < 10:
            # print(data)
            count_smooth += 1
        if count_smooth == 10:
            break
    # print(rank)
    return y_shake_data[rank - 9:], rank - 9


def insert(x_data, y_data):
    x = []
    for i in range(1, len(x_data) * 5 + 1, 5):
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
    # print(r)
    # print(11 - r)
    # print(angle)
    return r, angle


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
        print("observer get")
        # request.session['observer'] = observer
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
    num = 0
    average_grade = 0
    quadrant = [0, 0, 0, 0]
    right_up = 0
    left_up = 0
    left_blow = 0
    right_blow = 0
    grades = ""
    r_pos = ""
    p_pos = ""
    hearts = ""
    if request.method == 'POST':
        report_id = request.POST['report_id']
        # print(report_id)
        ids = report_id.split(",")
        for id in ids:
            # print(id)
            num += 1
            report = shoot_report.objects.get(id=id)
            grade = int(report.remark)
            grades += report.remark + ","
            total_grade += grade
            if grade > best_grade:
                best_grade = grade
            if grade < bad_grade:
                bad_grade = grade
            shoot_reports.append(report)
            shoot_grades = shoot_grade.objects.filter(report_id=id)
            heart_temp = []
            heart_total = 0
            for grade in shoot_grades:
                x = float(grade.x_pos)
                y = float(grade.y_pos)
                r, p = cart_to_polar(x, y)
                r = 11 - r
                r_pos += str(r) + ","
                p_pos += str(p) + ","
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
            hearts += str(heart) + ","
        average_grade = total_grade / num
    grades = grades[:-1]
    r_pos = r_pos[:-1]
    p_pos = p_pos[:-1]
    hearts = hearts[:-1]
    return render(request, 'sport_game_analyse.html', {
        'shoot_reports': shoot_reports,
        'best_grade': best_grade,
        'bad_grade': bad_grade,
        'average_grade': average_grade,
        'quadrant': quadrant,
        'right_up': right_up,
        'left_up': left_up,
        'left_blow': left_blow,
        'right_blow': right_blow,
        'grades': grades,
        'r_pos': r_pos,
        'p_pos': p_pos,
        'hearts': hearts
    })


def sport_game_analyse_id(request):
    report_id = request.GET['id']
    report = shoot_report.objects.get(id=report_id)
    grades = ""
    hearts = ""
    r_pos = ""
    p_pos = ""
    x_pos = ""
    y_pos = ""
    shoot_grades = shoot_grade.objects.filter(report_id=report_id).order_by('grade_detail_time')
    rapid_data = []
    for grade in shoot_grades:
        rapid_data.append(grade.rapid_time)
        grades += grade.grade + ","
        x_pos += grade.x_pos + ","
        y_pos += grade.y_pos + ","
        x = float(grade.x_pos)
        y = float(grade.y_pos)
        r, p = cart_to_polar(x, y)
        r = 11 - r
        r_pos += str(r) + ","
        p_pos += str(p) + ","
        hearts += str(grade.heart_rate) + ","
    grades = grades[:-1]
    hearts = hearts[:-1]
    r_pos = r_pos[:-1]
    p_pos = p_pos[:-1]

    x_data_plus = ""
    x_data_ori = ""
    y_data_plus = ""
    y_data_ori = ""

    x_up_data_plus = ""
    x_up_data_ori = ""
    y_up_data_plus = ""
    y_up_data_ori = ""

    y_shoot_pos = ""
    x_shoot_pos = ""

    x_pos_str = ""
    y_pos_str = ""

    x_shake_data = report.x_shake_data
    y_shake_data = report.y_shake_data
    x_up_shake_data = report.x_up_shake_data
    y_up_shake_data = report.y_up_shake_data
    if x_shake_data is not None and y_shake_data is not None:
        x_data = x_shake_data.split(",")
        y_data = y_shake_data.split(",")
        x_up_data = x_up_shake_data.split(",")
        y_up_data = y_up_shake_data.split(",")

        x_data = get_int_data(x_data)
        y_data = get_int_data(y_data, is_negative=True)
        x_up_data = get_int_data(x_up_data)
        y_up_data = get_int_data(y_up_data, is_negative=True)
        # print(y_data)

        y_data, num = cut_shake_data(y_data)
        x_data = x_data[num:]
        x_up_data = x_up_data[num:]
        y_up_data = y_up_data[num:]
        nums = get_shoot_point(y_data, is_insert=True)

        x_data, y_data = insert(x_data, y_data)

        x_data_ori, x_data_plus = shake_data_process(x_data)
        y_data_ori, y_data_plus, y_shoot_pos, y_pos_array = shake_data_process(y_data, nums)

        x_up_data, y_up_data = insert(x_up_data, y_up_data)

        x_up_data_ori, x_up_data_plus, x_shoot_pos, x_pos_array = shake_data_process(x_up_data, nums)
        y_up_data_ori, y_up_data_plus = shake_data_process(y_up_data)
        # print(len(x_pos_array))
        # print(x_pos_array[0])
        for x_pos_a in x_pos_array:
            # print(len(x_pos_a))
            for x_d in x_pos_a:
                # d1 = x_d
                d1 = round(x_d - x_pos_a[len(x_pos_a) - 1], 2)
                x_pos_str += str(d1) + ","
            x_pos_str = x_pos_str[:-1] + "#"
        for y_pos_a in y_pos_array:
            # print(len(y_pos_a))
            for y_d in y_pos_a:
                # d1 = y_d
                d1 = round(y_d - y_pos_a[len(y_pos_a) - 1], 2)
                y_pos_str += str(d1) + ","
            y_pos_str = y_pos_str[:-1] + "#"
        # print(x_pos_str)
    return render(request, 'sport_game_analyse_id.html', {
        'shoot_reports': report,
        'grades': grades,
        'hearts': hearts,
        'r_pos': r_pos,
        'p_pos': p_pos,
        'x_pos': x_pos[:-1],
        'y_pos': y_pos[:-1],
        'shoot_info': shoot_grades,
        'x_data': x_data_plus[:-1],
        'y_data': y_data_plus[:-1],
        'x_data_ori': x_data_ori[:-1],
        'y_data_ori': y_data_ori[:-1],
        'x_data_pos': report.x_shake_pos,
        'y_data_pos': report.y_shake_pos,
        'x_up_data': x_up_data_plus[:-1],
        'y_up_data': y_up_data_plus[:-1],
        'x_up_data_ori': x_up_data_ori[:-1],
        'y_up_data_ori': y_up_data_ori[:-1],
        'x_up_data_pos': report.x_up_shake_pos,
        'y_up_data_pos': report.y_up_shake_pos,
        'x_shoot_pos': x_shoot_pos,
        'y_shoot_pos': y_shoot_pos,
        'x_pos_str': x_pos_str,
        'y_pos_str': y_pos_str,
    })


def sport_game_history(request):
    user_name = request.session.get('user', "")
    if request.method == 'GET':
        report = shoot_report.objects.last()
        shoot_reports = None
        date = None
        if report is not None:
            date = report.shoot_date
            shoot_reports = shoot_report.objects.filter(shoot_date=report.shoot_date).filter(user_name=user_name)
        return render(request, 'sport_game_history.html', {
            'shoot_reports': shoot_reports,
            'date1': date,
            'date2': date
        })
    else:
        date1 = request.POST['date1']
        date2 = request.POST['date2']
        shoot_reports = shoot_report.objects.filter(user_name=user_name).filter(shoot_date__gte=date1).filter(
            shoot_date__lte=date2)
        return render(request, 'sport_game_history.html', {
            'shoot_reports': shoot_reports,
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
