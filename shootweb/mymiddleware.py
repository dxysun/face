# from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
from django.shortcuts import render


class SimpleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # if request.session.get('user', None):
        #     pass
        # else:
        #     return redirect("login")
        if 'face' in request.path:
            pass
        elif request.path != '/shoot/login' and request.path != '/shoot/login_admin':
            user = request.session.get('user', None)
            if user:
                role = request.session.get('role')
                # print(request.path)
                # print(role)
                if 'api' in request.path:
                    pass
                elif role == 'admin':
                    print('in admin')
                    if 'admin' in request.path:
                        pass
                    else:
                        return redirect("/shoot/login")
                elif role == 'athlete':
                    if 'sport' in request.path:
                        pass
                    else:
                        return redirect("/shoot/login")
                else:
                    pass
            else:
                return redirect("/shoot/login")
