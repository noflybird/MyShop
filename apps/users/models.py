from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="用户名")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(max_length=11, null=True, blank=True,  verbose_name="电话号码")
    email = models.EmailField(max_length=100, default="", verbose_name="电子邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    邮件验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    email = models.EmailField(max_length=100, verbose_name="电子邮箱")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "邮件验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code



