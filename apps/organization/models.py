# -*- coding: utf-8 -*-
# 机构信息 数据模型 #

from datetime import datetime

from django.db import models


class CityList(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市描述")
    describe = models.TextField(verbose_name="城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrganization(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    tag = models.CharField(max_length=10, verbose_name="机构标签", default='')
    describe = models.TextField(verbose_name="机构描述")
    category = models.CharField(max_length=20,
                                choices=(("train_org", "培训机构"), ("personal", "个人"), ("university", "高校")),
                                verbose_name="机构类别", default="train_org")
    click_num = models.IntegerField(default=0, verbose_name="点击数量")
    students_num = models.IntegerField(default=0, verbose_name="学习人数")
    courses_num = models.IntegerField(default=0, verbose_name="课程数量")
    favourite_num = models.IntegerField(default=0, verbose_name="收藏数量")
    address = models.CharField(max_length=100, verbose_name="机构地址")
    city = models.ForeignKey(CityList, verbose_name="机构所在城市", on_delete=models.CASCADE, default="")
    images = models.ImageField(upload_to="organization/%Y/%m", verbose_name="机构封面", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "机构信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 机构教师数量
    def getTeachersNumber(self):
        return self.teacher_set.all().count()


class Teacher(models.Model):
    organization = models.ForeignKey(CourseOrganization, verbose_name="所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="教师名称")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="公司名称")
    work_position = models.CharField(max_length=50, verbose_name="工作职位")
    specialty = models.CharField(max_length=50, verbose_name="教学特点")
    click_num = models.IntegerField(default=0, verbose_name="点击数量")
    favourite_num = models.IntegerField(default=0, verbose_name="收藏数量")
    images = models.ImageField(upload_to="teachers/%Y/%m", verbose_name="讲师封面",
                               max_length=100, null=True, default='')
    is_approval = models.BooleanField(default=False, verbose_name='是否认证')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
