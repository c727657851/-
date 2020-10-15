from rest_framework import serializers
from .models import News,NewsCategory,Comment
from apps.cmsauth.serializers import UserSerializers

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('name',)

class NewsSerializers(serializers.ModelSerializer):

    author = UserSerializers()
    category = NewsCategorySerializer()
    class Meta:
        model = News
        fields = ('id','title','desc','thumbnail','pub_time','author','category')


class CommentSerializers(serializers.ModelSerializer):
    author = UserSerializers()
    class Meta:
        model = Comment
        fields = ('id','content','pub_time','author')

