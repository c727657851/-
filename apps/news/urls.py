from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('',views.index,name='index'),
    path('<int:news_id>/',views.news_detail,name='news_detail'),
    path('list/',views.news_list,name='news_list'),
    path('pub_comment/',views.public_comment,name='pub_comment'),
]