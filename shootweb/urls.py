# -*- coding:utf-8 -*- 
__author__ = 'dxy'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name="shoot_index_login"),
    url(r'^login$', views.login, name="shoot_login"),
    url(r'^login_admin$', views.login_admin, name="login_admin"),
    url(r'^logout', views.logout, name="shoot_logout"),
    url(r'^api/get_user_info$', views.get_user_info, name="get_user_info"),
    url(r'^api/test', views.test, name="shoot_test"),
    url(r'^register', views.register, name="shoot_register"),
    url(r'^sport/home', views.sport_home, name="sport_home"),
    url(r'^sport/game_analyse$', views.sport_game_analyse, name="sport_game_analyse"),
    url(r'^sport/game_analyse_id$', views.sport_game_analyse_id, name="sport_game_analyse_id"),
    url(r'^sport/game_history', views.sport_game_history, name="sport_game_history"),
    url(r'^coach/home$', views.coach_home, name="coach_home"),
    url(r'^coach/sport_info$', views.coach_sport_info, name="coach_sport_info"),
    url(r'^coach/game_info$', views.coach_game_info, name="coach_game_info"),
    url(r'^coach/sport_info_detail$', views.coach_sport_info_detail, name="coach_sport_info_detail"),
    url(r'^admin/home$', views.admin_home, name="admin_home"),
    url(r'^admin/item/add', views.admin_add_item, name="admin_add_item"),
    url(r'^admin/item/delete', views.admin_delete_item, name="admin_delete_item"),
    url(r'^admin/item/modify', views.admin_modify_item, name="admin_modify_item"),
    url(r'^admin/coach$', views.admin_coach, name="admin_coach"),
    url('^admin/coach/add', views.admin_add_coach, name="admin_add_coach"),
    url(r'^admin/coach/delete', views.admin_delete_coach, name="admin_delete_coach"),
    url(r'^admin/coach/modify', views.admin_modify_coach, name="admin_modify_coach"),
    url(r'^admin/sport$', views.admin_sport, name="admin_sport"),
    url(r'^admin/sport/add', views.admin_add_sport, name="admin_add_sport"),
    url(r'^admin/sport/delete', views.admin_delete_sport, name="admin_delete_sport"),
    url(r'^admin/sport/modify', views.admin_modify_sport, name="admin_modify_sport"),
    url(r'^admin/analyse$', views.admin_analyse, name="admin_analyse"),
]
