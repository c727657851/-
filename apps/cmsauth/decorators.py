from utils import restful
from django.shortcuts import redirect,reverse
from django.http import Http404

def cms_login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录')
            else:
                return redirect('/')
    return wrapper


def cms_supperuser_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_superuser:
            return func(request,*args,**kwargs)
        else:
            raise Http404
    return wrapper
