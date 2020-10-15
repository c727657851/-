from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField
# Create your models here.

class UserManger(BaseUserManager):
    def _create_user(self, telephone,username, password, email=None, **kwargs):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('请输入用户名')
        if not telephone:
            raise ValueError('请输入手机号')
        if not password:
            raise ValueError('请输入密码')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(telephone=telephone, username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, email=None, **kwargs):
        kwargs['is_staff'] = False
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, email=email, **kwargs)

    def create_superuser(self, telephone,username, password,email=None, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self._create_user(telephone, username, password, email=email, **kwargs)

class User(AbstractBaseUser,PermissionsMixin):
    # 不适用自增的主键
    # 使用UUID  安装 pip install django-shortuuidfield
    # 导入from shortuuidfield import ShortUUIDField
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11,unique=True, validators=[validators.RegexValidator(r'1[3-9]\d{9}', message='请输入正确的手机号')])
    email = models.EmailField(null=True)
    username = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    thumbnail = models.URLField(default='http://qe0l8lesp.bkt.clouddn.com/1595858988624.jfif')
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']

    objects = UserManger()

    # 用户的完整的代码
    def get_full_name(self):
        return self.username

    # 获取拉黑用户的方法
    def get_black_user(self):
        return self.objects.filter(is_active=False)

