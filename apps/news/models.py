from django.db import models

# Create your models here.
class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()   # 存放缩略图的地址
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('NewsCategory',on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey('cmsauth.User',on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ['-pub_time']


class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('News',on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey('cmsauth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']


