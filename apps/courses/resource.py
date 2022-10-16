# -*- coding: utf-8 -*-

from import_export import resources

from apps.courses.models import Courses, Lessons, Videos, CourseDownload, CarouselBanner


class CoursesResource(resources.ModelResource):
    class Meta:
        model = Courses


class LessonResource(resources.ModelResource):
    class Meta:
        model = Lessons


class VideoResource(resources.ModelResource):
    class Meta:
        model = Videos


class CourseDownloadResource(resources.ModelResource):
    class Meta:
        model = CourseDownload


class CarouselBannerResource(resources.ModelResource):
    class Meta:
        model = CarouselBanner
