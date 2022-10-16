# -*- coding: utf-8 -*-
# 系统操作 数据模型 #

from datetime import datetime

from django.db import models

from apps.courses.models import Courses
from apps.users.models import UserProfile


# 用户咨询
class UserAsk(models.Model):
    user = models.CharField(max_length=10, verbose_name="用户信息")
    telephone = models.CharField(max_length=11, verbose_name='电话', null=True, blank=True)
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


# 用户收藏
class UserFavourite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户信息", on_delete=models.CASCADE)
    favourite_id = models.IntegerField(default=0, verbose_name="收藏信息id")
    favourite_type = models.IntegerField(choices=((1, "课程"), (2, "机构"), (3, "讲师")), verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


# 站内消息
class UserMessage(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户信息", on_delete=models.CASCADE)
    title = models.CharField(max_length=30, verbose_name="消息标题", default='')
    content = models.TextField(max_length=500, verbose_name="消息内容", default='')
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="消息时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 用户学习课程
class UserCourses(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户信息", on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, verbose_name="用户课程", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


# 用户评论
class UserCoursesComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户信息", on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, verbose_name="用户课程", on_delete=models.CASCADE)
    comments = models.TextField(max_length=300, verbose_name="用户评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
