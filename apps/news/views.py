from django.shortcuts import render
from apps.news.models import NewsCategory,News
from django.conf import settings
from django.http import Http404
from .serializers import NewsSerializers,CommentSerializers
from utils import restful
from .forms import PublicCommentForm
from .models import Comment

# Create your views here.
def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category','author').all()[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
    }
    return render(request,'news/index.html',context=context)

def news_detail(request,news_id):
    try:
        news = News.objects.select_related('category','author').prefetch_related('comments').get(pk=news_id)
        context = {
            'news': news
        }
        return render(request,'news/news_detail.html',context=context)
    except News.DoesNotExist:
        raise Http404

def news_list(request):

    #通过 p参数 获取用户想查看第几页
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))

    #1 0 1  2
    #2 2 3  4
    #3 4 5  6
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0:
        newses = News.objects.select_related('category','author').all()[start:end]
    else:
        newses = News.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]

    serializer = NewsSerializers(newses,many=True)  # 每一条都要序列化成json
    data = serializer.data
    return restful.result(data=data)

# 评论
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comments = Comment.objects.create(content=content,news=news,author=request.user)
        serializer = CommentSerializers(comments)
        data = serializer.data
        return restful.result(data=data)
    else:
        return restful.params_error(message=form.get_errors)