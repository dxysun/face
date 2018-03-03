# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import face_functions as face
import os
import time
import json
from .models import user_info, image_info, game_info
# Create your views here.


def check_session(request):
    username = request.session.get("username", None)
    print("check_session " + str(username))
    if username is None:
        return False
    else:
        return True


def index(request):
    if not check_session(request):
        return redirect("/face/login/")
    return render(request, 'index.html')


def home(request):
    if not check_session(request):
        return redirect("/face/login/")
    return render(request, 'home.html')


def user_login(request):
    return render(request, 'login.html')


def user_logout(request):
    del request.session['username']
    return redirect("/face/login/")


def login_check(request):
    result = {}
    if request.method == "POST":  # 请求方法为POST时，进行处理
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        print(str(username) + "  " + str(password))
        user = user_info.objects.filter(username=username)
        print(str(user))
        if len(user) == 0:
            result["status"] = "failed"
        elif user[0].password == password:
            request.session["username"] = username
            request.session["userid"] = user[0].id
            result["status"] = "success"
        else:
            result["status"] = "failed"
            result['error_message'] = "密码或用户名错误"
    return JsonResponse(result)


def set_session(request):
    result = {}
    if request.method == "POST":  # 请求方法为POST时，进行处理
        username = request.POST.get("username", None)
        if username is None:
            result["status"] = "failed"
            result['error_message'] = "未登录，请登录"
        else:
            request.session["username"] = username
            result["status"] = "success"
    return JsonResponse(result)


def username_check(request):
    result = {}
    if request.method == "POST":  # 请求方法为POST时，进行处理
        username = request.POST.get("username", None)
        user = user_info.objects.filter(username=username)
        print(str(user))
        if len(user) == 0:
            result["status"] = "not_exist"
        else:
            result["status"] = "exist"
    return JsonResponse(result)


def register(request):
    return render(request, 'register.html')


def register_finished(request):
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    print(str(username) + "  " + str(password))
    user = user_info(username=username, password=password)
    user.save()
    path = "D:\\workSpace\\PythonWorkspace\\face\\face_bit/static/userinfo/user" + str(user.id) + "/"
    print("path:" + path)
    if not os.path.exists(path):
        os.makedirs(path)
    info = face.face_create(username, "face_game_users")
    if info.get("status") == "success":
        print("crate face success")
    return redirect("/face/login/")


def recognition(request):
    if not check_session(request):
        return redirect("/face/login/")
    return render(request, 'recognition.html')


def detect(request):
    if not check_session(request):
        return redirect("/face/login/")
    return render(request, 'detect.html')


def face_detect(request):
    if not check_session(request):
        return redirect("/face/login/")
    return render(request, 'face_detect.html')


def face_result(request):
    if not check_session(request):
        return redirect("/face/login/")
    if request.method == "GET":
        img_id = request.GET.get("id", None)
        image = image_info.objects.get(id=img_id)
    return render(request, 'face_result.html', {
        "img": image
    })


def face_recognition(request):
    if not check_session(request):
        return redirect("/face/login/")
    return render(request, 'face_recognition.html')


def face_planegame(request):
    if not check_session(request):
        return redirect("/face/login/")
    game_score = game_info.objects.all().order_by('-score')[:5]

    return render(request, 'face_planegame.html', {
        "game_score": game_score,
        "length": len(game_score)
    })


def game_rank(request):
    if not check_session(request):
        return redirect("/face/login/")
    username = request.session.get("username", None)
    game_score = game_info.objects.all().order_by('-score')
    user_score = game_info.objects.filter(username=username).order_by('-score')
    result = {}
    if len(user_score) > 0:
        i = 1
        for game in game_score:
            if game.id == user_score[0].id:
                result["user_score"] = game.score
                result["user_rank"] = i
            i += 1
    games = game_score[:10]
    result["game_score"] = games
    result["game_length"] = len(games)
    return render(request, 'game_rank.html', result)


def history_score(request):
    if not check_session(request):
        return redirect("/face/login/")
    username = request.session.get("username", None)
    user_score = game_info.objects.filter(username=username).order_by('-score')
    return render(request, 'history_score.html', {
        "user_score": user_score
    })


def record_score(request):
    if not check_session(request):
        return redirect("/face/login/")
    username = request.session.get("username", None)
    score = request.POST.get("score", None)
    result = {}
    date_score = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    game = game_info(username=username, score=score, date_score=str(date_score))
    game.save()
    result['status'] = "success"
    return JsonResponse(result)


def face_webcam(request):
    if not check_session(request):
        return redirect("/face/login/")
    username = request.session.get("username", None)
    user = user_info.objects.get(username=username)
    if user.img_url == "":
        return redirect("/face/face_upload/")
    return render(request, 'face_webcam.html')


def face_upload(request):
    if not check_session(request):
        return redirect("/face/login/")
    return render(request, 'face_upload.html')


def myinfo(request):
    if not check_session(request):
        return redirect("/face/login/")
    username = request.session.get("username", None)
    user = user_info.objects.get(username=username)
    return render(request, 'myinfo.html', {
        'user': user
    })


def myphoto(request):
    if not check_session(request):
        return redirect("/face/login/")
    username = request.session.get("username", None)
    imgs = image_info.objects.filter(username=username)
    not_remark = []
    remark = []
    recognize = []
    for img in imgs:
        if img.img_type == 0:
            not_remark.append(img)
        if img.img_type == 1:
            remark.append(img)
        if img.img_type == 2:
            recognize.append(img)
    return render(request, 'myphoto.html', {
        'not_remark': not_remark,
        'remark': remark,
        'recognize': recognize
    })


def test(request):
    if not check_session(request):
        return redirect("/face/login/")
    return render(request, 'face_game.html')


def mysocket(request):
    if not check_session(request):
        return redirect("/face/login/")
    return render(request, 'socket.html')


def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        print("server start")
        username = request.session.get("username", None)
        userid = request.session.get("userid", None)
        print(username)
        detect_type = request.POST.get("detect_type", None)
        print("detect_type: " + str(detect_type))
        my_file = request.FILES.get("detectfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        result = {}
        if not my_file:
            result['status'] = "failed"
            return JsonResponse(result)
        path = "D:\\workSpace\\PythonWorkspace\\face\\face_bit/static/userinfo/user" + str(userid) + "/photos/"
        # path = "/static/userinfo/" + username + "/photos/"
        if not os.path.exists(path):
            os.makedirs(path)
        img = image_info(username=username)
        img.save()
        my_file.name = "photo" + str(img.id) + os.path.splitext(my_file.name)[1]
        destination = open(os.path.join(path, my_file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in my_file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        print("server my_file.name  " + my_file.name)
        img_url = path + my_file.name
        file = open(img_url, 'rb')
        print("server face_detect")
        # result = face.face_detect(file)
        print("goto face_result   ")
        result = face.face_detect(file)
        img_url = img_url[42:]
        if result.get("error_message") is None:
            faces = result.get("faces")
            if detect_type == "detect":
                print("img detect start " + str(img_url))
                result_info = json.dumps(result, ensure_ascii=False)
                # img = image_info(img_url=img_url, username=username, remark=str(result_info))
                img.img_url = img_url
                img.remark = str(result_info)
                if len(faces) == 1:
                    img.face_token = faces[0].get("face_token")
                img.save()
                print("img save")
            else:
                names = ""
                for face_info in faces:
                    info = face.face_serach(username, face_info.get("face_token"))
                    face_info["face_name"] = info.get("name")
                    names += info.get("name") + " "
                result_info = json.dumps(result, ensure_ascii=False)
                print(result_info)
                img.img_url = img_url
                img.img_label = names
                img.img_type = 2
                img.remark = result_info
                img.save()
            result['img_id'] = img.id
            result['filepath'] = img_url
            result['status'] = "success"
        else:
            result['status'] = "failed"
            result['error_message'] = str(result.get("error_message")) + ",请稍后重试"
            image_info.objects.filter(id=img.id).delete()
        print("face_result out  ")
        return JsonResponse(result)


def recognize_again(request):
    if request.method == "POST":
        username = request.session.get("username", None)
        img_id = request.POST.get("img_id", None)
        print("img_id:" + img_id)
        img = image_info.objects.get(id=img_id)
        img_info = eval(img.remark)
        faces = img_info["faces"]
        names = ""
        for face_info in faces:
            info = face.face_serach(username, face_info["face_token"])
            face_info["face_name"] = info["name"]
            names += info.get("name") + " "
        img.img_label = names
        img.img_type = 2
        result_info = json.dumps(img_info, ensure_ascii=False)
        img.remark = result_info
        img.save()
        img_info['img_id'] = img.id
        img_info['filepath'] = img.img_url
        img_info['status'] = "success"
        return JsonResponse(img_info)


def remark_photo(request):
    if request.method == "POST":
        username = request.session.get("username", None)
        result = {}
        img_id = request.POST.get("img_id", None)
        label = request.POST.get("label", None)
        print("img_id " + str(img_id))
        img = image_info.objects.get(id=img_id)
        img.img_label = label
        img.img_type = 1
        img.save()
        print("save end")
        info = face.face_add(username, img.face_token, label)
        if info["status"] == "success":
            print("add face success")
            result['status'] = "success"
        else:
            result['status'] = "failed"
            result['error_message'] = "标记照片失败，请稍后重试"
        return JsonResponse(result)


def update_info(request):
    username = request.session.get("username", None)
    update_type = request.POST.get("update_type", None)
    user = user_info.objects.get(username=username)
    result = {}
    if update_type == "password":
        origin_pw = request.POST.get("origin_pw", None)
        new_pw = request.POST.get("new_pw", None)
        print(new_pw)
        if user.password == origin_pw:
            user.password = new_pw
            user.save()
            result['status'] = "success"
        else:
            result['status'] = "failed"
            result['error_message'] = "密码更新失败，请稍后重试"
    else:
        my_file = request.FILES.get("detectfile", None)
        if my_file is not None:
            path = "D:\\workSpace\\PythonWorkspace\\face\\face_bit/static/userinfo/user" + str(user.id) + "/"
            if not os.path.exists(path):
                os.makedirs(path)
            my_file.name = "user" + str(user.id) + os.path.splitext(my_file.name)[1]
            destination = open(os.path.join(path, my_file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in my_file.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            detect_file = open(path + my_file.name, 'rb')
            result = face.face_detect(detect_file)
            faces = result.get("faces")
            if len(faces) == 1:
                if user.img_url != "":
                    face.delete_face(username, user.face_token)
                img_url = "/static/userinfo/user" + str(user.id) + "/" + my_file.name
                result['img_url'] = img_url
                user.img_url = img_url
                user.face_token = faces[0].get("face_token")
                faces[0]["face_name"] = username
                user.remark = json.dumps(result, ensure_ascii=False)
                user.save()
                face.face_add(username, faces[0].get("face_token"), username)
                result['status'] = "success"
            else:
                result['status'] = "failed"
                result['error_message'] = "请上传包含一个人脸的个人美照"
        else:
            result['status'] = "failed"
            result['error_message'] = "上传的文件为空"
    return JsonResponse(result)
