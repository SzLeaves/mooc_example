from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.courses.models import Courses, Lessons, Videos, CourseDownload, CarouselBanner
from apps.courses.resource import CourseDownloadResource, CarouselBannerResource
from apps.courses.resource import CoursesResource, LessonResource, VideoResource


class CoursesAdmin(ImportExportModelAdmin):
    list_display = ('name', 'describe', 'students_num', 'favourite_num', 'click_num', 'add_time')
    list_filter = ['name', 'difficulty', 'study_times', 'students_num', 'favourite_num', 'images',
                   'click_num', 'add_time']
    search_fields = ['name', 'describe', 'detail', 'difficulty', 'study_times', 'students_num', 'favourite_num',
                     'images', 'click_num']
    resource_class = CoursesResource


class LessonsAdmin(ImportExportModelAdmin):
    list_display = ('course', 'name', 'add_time')
    list_filter = ['course', 'name', 'add_time']
    search_fields = ['course', 'name', 'add_time']
    resource_class = LessonResource


class VideosAdmin(ImportExportModelAdmin):
    list_display = ('lesson', 'name', 'url', 'add_time')
    list_filter = ['lesson', 'name', 'url', 'add_time']
    search_fields = ['lesson', 'name', 'url', 'add_time']
    resource_class = VideoResource


class CourseDownloadAdmin(ImportExportModelAdmin):
    list_display = ('course', 'name', 'path', 'add_time')
    list_filter = ['course', 'name', 'path', 'add_time']
    search_fields = ['course', 'name', 'path', 'add_time']
    resource_class = CourseDownloadResource


class CarouselBannerAdmin(ImportExportModelAdmin):
    list_display = ('title', 'image', 'path', 'index', 'add_time')
    list_filter = ['title', 'image', 'path', 'index', 'add_time']
    search_fields = ['title', 'image', 'path', 'index', 'add_time']
    resource_class = CarouselBannerResource


admin.site.register(Courses, CoursesAdmin)
admin.site.register(Lessons, LessonsAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(CourseDownload, CourseDownloadAdmin)
admin.site.register(CarouselBanner, CarouselBannerAdmin)

# admin界面设置
# 页面标题
admin.site.site_header = "后台管理系统"
# 标签栏标题
admin.site.site_title = "后台管理系统"
