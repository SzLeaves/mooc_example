# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.organization.models import CityList
from apps.organization.models import CourseOrganization
from apps.organization.models import Teacher
from apps.organization.resource import CityListResource
from apps.organization.resource import CourseOrganizationResource
from apps.organization.resource import TeacherResource


class CityListAdmin(ImportExportModelAdmin):
    list_display = ('name', 'describe', 'add_time')
    list_filter = ['name', 'describe', 'add_time']
    search_fields = ['name', 'describe', 'add_time']
    resource_class = CityListResource


class CourseOrganizationAdmin(ImportExportModelAdmin):
    list_display = ('name', 'describe', 'address', 'click_num', 'favourite_num', 'add_time')
    list_filter = ['name', 'describe', 'address', 'click_num', 'favourite_num', 'add_time']
    search_fields = ['name', 'describe', 'address', 'click_num', 'favourite_num', 'add_time']
    resource_class = CourseOrganizationResource


class TeacherAdmin(ImportExportModelAdmin):
    list_display = ('name', 'organization', 'work_years', 'work_position', 'add_time')
    list_filter = ['name', 'organization', 'work_years', 'work_position', 'specialty', 'add_time']
    search_fields = ['name', 'organization', 'work_years', 'work_position', 'specialty', 'add_time']
    resource_class = TeacherResource


#  注册模型
admin.site.register(CityList, CityListAdmin)
admin.site.register(CourseOrganization, CourseOrganizationAdmin)
admin.site.register(Teacher, TeacherAdmin)

# admin界面设置
# 页面标题
admin.site.site_header = "后台管理系统"
# 标签栏标题
admin.site.site_title = "后台管理系统"
