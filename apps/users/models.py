# -*- coding: utf-8 -*-
# 个人用户信息 数据模型 #

from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# 用户信息
class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, verbose_name="昵称", default='')
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default='', verbose_name="性别")
    address = models.CharField(max_length=100, verbose_name="地址", default='')
    telephone = models.CharField(max_length=11, verbose_name='电话', null=True, blank=True, default='')
    image = models.ImageField(max_length=100, upload_to="image/%Y/%m", default="image/default.png",
                              verbose_name="用户头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # 获取用户未读消息数量
    def getUnreadNum(self):
        return self.usermessage_set.filter(is_read=False).count()


# 邮箱验证功能
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("forget", "找回密码"), ("update", "修改邮箱")),
                                 max_length=10,
                                 verbose_name="验证类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.email, self.code)
