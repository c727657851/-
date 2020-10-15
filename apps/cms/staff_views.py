from apps.cmsauth.models import User
from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from django.contrib.auth.models import Group
from django.contrib import messages
from apps.cmsauth.decorators import cms_supperuser_required
from django.utils.decorators import method_decorator

@cms_supperuser_required
def staff_views(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs':staffs
    }

    return render(request,'cms/staffs.html',context=context)

@method_decorator(cms_supperuser_required,name='dispatch')
class AddStaffView(View):
    def get(self,request):
        groups = Group.objects.all()
        context = {
            'groups':groups
        }
        return render(request,'cms/add_staff.html',context=context)

    def post(self,request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        if user:
            user.is_staff = True
            group_ids = request.POST.getlist('groups')    # getlist接收多个参数
            group = Group.objects.filter(pk__in=group_ids)
            user.groups.set(group)
            user.save()
            return redirect(reverse('cms:staffs'))
        else:
            messages.info(request,'手机号码不存在')
            return redirect(reverse('cms:staffs'))

