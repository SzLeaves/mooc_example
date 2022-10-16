# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.operation.models import UserAsk, UserFavourite, UserMessage, UserCourses, UserCoursesComments
from apps.operation.resource import UserAskResource, UserCoursesResource
from apps.operation.resource import UserCoursesCommentsResource, UserFavouriteResource, UserMessageResource


class UserAskAdmin(ImportExportModelAdmin):
    list_display = ('user', 'telephone', 'course_name', 'add_time')
    list_filter = ['user', 'telephone', 'course_name', 'add_time']
    search_fields = ['user', 'telephone', 'course_name', 'add_time']
    resource_class = UserAskResource


class UserFavouriteAdmin(ImportExportModelAdmin):
    list_display = ('user', 'favourite_id', 'favourite_type', 'add_time')
    list_filter = ['user', 'favourite_id', 'favourite_type', 'add_time']
    search_fields = ['user', 'favourite_id', 'favourite_type', 'add_time']
    resource_class = UserFavouriteResource


class UserMessageAdmin(ImportExportModelAdmin):
    list_display = ('user', 'title', 'is_read', 'add_time')
    list_filter = ['user', 'title', 'is_read', 'add_time']
    search_fields = ['user', 'title', 'is_read', 'add_time']
    resource_class = UserMessageResource


class UserCoursesAdmin(ImportExportModelAdmin):
    list_display = ('user', 'course', 'add_time')
    list_filter = ['user', 'course', 'add_time']
    search_fields = ['user', 'course', 'add_time']
    resource_class = UserCoursesResource


class UserCoursesCommentAdmin(ImportExportModelAdmin):
    list_display = ('user', 'course', 'comments', 'add_time')
    list_filter = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments', 'add_time']
    resource_class = UserCoursesCommentsResource


admin.site.register(UserAsk, UserAskAdmin)
admin.site.register(UserFavourite, UserFavouriteAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(UserCourses, UserCoursesAdmin)
admin.site.register(UserCoursesComments, UserCoursesCommentAdmin)

# admin界面设置
# 页面标题
admin.site.site_header = "后台管理系统"
# 标签栏标题
admin.site.site_title = "后台管理系统"
