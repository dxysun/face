# -*- coding: utf-8 -*-
from django.conf import settings


# 得到语言设置

def globar_var(request):
    if request.session.get('user', None):
        # print(request.session.get('user'))
        return {
            'user': request.session.get('user'),
            'role': request.session.get('role'),
            'user_id': request.session.get('user_id')
        }
    else:
        return {
            'sole': 'None'
        }
