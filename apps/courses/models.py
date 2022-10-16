# -*- coding: utf-8 -*-
# 课程信息 数据模型 #

from datetime import datetime

from django.db import models

from apps.organization.models import CourseOrganization, Teacher


# 课程信息
class Courses(models.Model):
    name = models.CharField(max_length=50, verbose_name="课程名")
    teachers = models.ForeignKey(Teacher, verbose_name='课程讲师',
                                 on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(CourseOrganization, verbose_name="课程机构",
                                     on_delete=models.CASCADE, null=True, blank=True)
    describe = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    is_carousel = models.BooleanField(default=False, verbose_name="是否作为广告位轮播图")
    difficulty = models.CharField(choices=(("primary", "初级"), ("intermediate", "中级"), ("advanced", "高级")),
                                  max_length=15, verbose_name="课程难度")
    study_times = models.IntegerField(default=0, verbose_name="学习时间")
    students_num = models.IntegerField(default=0, verbose_name="学习人数")
    favourite_num = models.IntegerField(default=0, verbose_name="收藏数量")
    images = models.ImageField(upload_to="courses/%Y/%m", verbose_name="课程封面", max_length=100)
    click_num = models.IntegerField(default=0, verbose_name="课程点击量")
    category = models.CharField(default='', max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='', max_length=50, verbose_name='课程推荐标签')
    notice = models.CharField(default='', max_length=300, verbose_name='课程须知', null=True, blank=True)
    knowledge = models.CharField(default='', max_length=300, verbose_name='课程知识点', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取课程章节
    def getChapter(self):
        return self.lessons_set.all()

    # 获取课程章节数
    def getChapterNumber(self):
        return self.lessons_set.all().count()

    # 获取学习用户(前5)
    def getUserCourses(self):
        return self.usercourses_set.all()[:5]


# 章节信息
class Lessons(models.Model):
    course = models.ForeignKey(Courses, verbose_name="课程信息", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="章节名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取课程视频
    def getLessonsVideo(self):
        return self.videos_set.all()


# 视频信息
class Videos(models.Model):
    lesson = models.ForeignKey(Lessons, verbose_name="章节名称", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="视频名称")
    url = models.URLField(default='', verbose_name='访问地址')
    times = models.IntegerField(default=0, verbose_name="视频时长")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程资源
class CourseDownload(models.Model):
    course = models.ForeignKey(Courses, verbose_name="课程信息", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="资源名称")
    path = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="资源路径")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 轮播图
class CarouselBanner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.FileField(upload_to="course/carousel/%Y/%m", verbose_name="图片路径")
    path = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=0, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
