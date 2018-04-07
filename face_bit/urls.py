# -*- coding:utf-8 -*-
__author__ = 'lenovo'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^$', views.home, name="home"),
    url(r'^recognition/$', views.recognition, name="recognition"),
    url(r'^face_recognition/$', views.face_recognition, name="face_recognition"),
    url(r'^recognize_again/$', views.recognize_again, name="recognize_again"),
    url(r'^detect/$', views.detect, name="detect"),
    url(r'^face_detect/$', views.face_detect, name="face_detect"),
    url(r'^face_result', views.face_result, name="face_result"),
    url(r'^remark_photo/$', views.remark_photo, name="remark_photo"),
    url(r'^face_planegame/$', views.face_planegame, name="face_planegame"),
    url(r'^game_rank/$', views.game_rank, name="game_rank"),
    url(r'^history_score/$', views.history_score, name="history_score"),
    url(r'^record_score/$', views.record_score, name="record_score"),
    url(r'^face_webcam/$', views.face_webcam, name="face_webcam"),
    url(r'^face_upload/$', views.face_upload, name="face_upload"),
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.user_login, name="login"),
    url(r'^myinfo/$', views.myinfo, name="myinfo"),
    url(r'^update_info/$', views.update_info, name="update_info"),
    url(r'^myphoto/$', views.myphoto, name="myphoto"),
    url(r'^set_session/$', views.set_session, name="set_session"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^login_check/$', views.login_check, name="login_check"),
    url(r'^username_check/$', views.username_check, name="username_check"),
    url(r'^register_finished/$', views.register_finished, name="register_finished"),
    url(r'^upload/$', views.upload_file, name="upload"),
    url(r'^test/$', views.test, name="test"),
    url(r'^socket/$', views.mysocket, name="socket"),
    url(r'^visitor_login/$', views.visitor_login, name="visitor_login"),
]
