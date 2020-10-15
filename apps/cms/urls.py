from django.urls import path
from . import views,staff_views

app_name = 'cms'

urlpatterns = [
    path('',views.index,name='index'),
    path('write_news/',views.WriteNews.as_view(),name='write_news'),
    path('news_category/',views.news_category,name='news_category'),
    path('add_news_category/',views.add_news_category,name='add_news_category'),
    path('qntoken/',views.qntoken,name='qntoken'),
    path('my_login/',views.my_login,name='my_login'),
    path('MyYogin/',views.login_view,name='MyYogin'),
    path('news_list/',views.NewsList.as_view(),name='news_list'),
]

urlpatterns += [
    path('staffs/',staff_views.staff_views,name='staffs'),
    path('add_staff/',staff_views.AddStaffView.as_view(),name='add_staff')
]
