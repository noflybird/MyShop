# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import VerifyCode
from MyShop.settings import REG_EMAIL

User = get_user_model()


class SmsCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    def validate_email(self, email):
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError("该邮箱已注册")
        if not re.match(REG_EMAIL, email):
            raise serializers.ValidationError("邮箱非法")
        minutes_1_go = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=minutes_1_go, email=email).count():
            raise serializers.ValidationError("距离上一次发送未超过1分钟")
        return email


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("name", "gender", "mobile", "birthday", "email")


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册
    """
    code = serializers.CharField(max_length=6, min_length=6, write_only=True,
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }, help_text="验证码", label="验证码")
    username = serializers.CharField(required=True, allow_blank=False, help_text="用户名", label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="该用户存在")])
    password = serializers.CharField(
        style={"input_type": "password"},
        label="密码",
        help_text="密码",
        write_only=True
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(email=self.initial_data["email"]).order_by("-add_time")
        if verify_records:
            last_records = verify_records[0]
            minutes_10_go = datetime.now() - timedelta(hours=0, minutes=10, seconds=0)
            if minutes_10_go > last_records.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_records.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "email", "code",  "password")
