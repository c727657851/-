from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from apps.news.models import NewsCategory,News
from utils import restful
from apps.cms.forms import WriteNewsForm
from django.views.decorators.http import require_GET,require_POST
import qiniu
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
from django.utils.decorators import method_decorator  #权限装饰器
from django.contrib.auth.decorators import permission_required

from apps.cmsauth.forms import LoginForm
from django.contrib.auth import login,authenticate
# Create your views here.

def index(request):
    return render(request,'cms/index.html')


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')

        user = authenticate(request, username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)  # 默认保存两周
                else:
                    request.session.set_expiry(0)

                return redirect(reverse('cms:index'))
            else:
                return restful.unauth(message='您的账号未激活')
        else:
            return restful.params_error(message='手机号或者密码错误')
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)


# 列出文章
@method_decorator(permission_required(perm="news.view_news",login_url='/'),name='dispatch')   # 前面是模型的名字
class NewsList(View):
    def get(self,request):
        page = int(request.GET.get('p',1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category',0) or 0)
        newses = News.objects.select_related('category','author')
        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2019,month=6,day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))
        if title:
            newses = newses.filter(title__icontains=title)
        if category_id:
            newses = newses.filter(category=category_id)


        paginator = Paginator(newses,2)
        page_obj = paginator.page(page)
        context_data = self.get_pagination_data(paginator,page_obj)
        context = {
            'newses':page_obj.object_list,  # 根据分页展示
            'paginator': paginator,
            'page_obj': page_obj,
            'categories': NewsCategory.objects.all(),
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({   # 将字典转换成 &start=&end=&title&category
                'start': start or '',
                'end':end or '',
                'title':title or '',
                'category':category_id or '',
            })
        }
        context.update(context_data)  # 更新数据
        return render(request,'cms/news_list.html',context=context)

    def get_pagination_data(self,paginator,page_obj,arround_count=2):
        current_page = page_obj.number  # 当前页码
        number_pages = paginator.num_pages  # 总共页数

        left_has_more = False
        right_has_more = False

        if current_page<=arround_count+2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(number_pages-arround_count,current_page)

        if current_page>=number_pages-arround_count-1:
            right_pages = range(current_page+1,number_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+arround_count+1)

        return {
            'left_pages':left_pages,
            'right_pages':right_pages,
            'current_page':current_page,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'number_pages':number_pages,
        }


def my_login(request):
    return render(request,'cms/login.html')

@method_decorator(permission_required(perm="news.add_news",login_url='/'),name='dispatch')   # 前面是模型的名字
class WriteNews(View):
    def get(self,request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'cms/write_news.html',context=context)

    def post(self,request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title,desc=desc,category=category,thumbnail=thumbnail,content=content,author=request.user)
            return restful.success()
        else:
            return restful.params_error(message=form.get_errors())



@permission_required(perm='news_view_newscategory',login_url='/')
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request,'cms/news_category.html', context=context)

@permission_required(perm='news.add_newscategory',login_url='/')
def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if exists:
        return restful.params_error(message='该分类以及存在')
    else:
        NewsCategory.objects.create(name=name)
        return restful.success()


@require_GET
def qntoken(request):
    access_key = 'UGn4NbCEOYgQ4mAa40VSoKf2CF5UtpDGhrDyMrNG'
    secret_key = 'VVB7j9NWeegSrO8uccmqPh4620OmFi6gCSprboO1'
    q = qiniu.Auth(access_key, secret_key)

    bucket = 'cuizhihao'   # 存储空间
    token = q.upload_token(bucket)
    return restful.result(data={"token":token})