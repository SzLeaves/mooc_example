# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.users.models import EmailVerifyRecord
from apps.users.models import UserProfile
from apps.users.resource import UserProfileResource
from apps.users.resource import VerifyRecordResource


class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'username', 'nickname', 'address', 'telephone')
    list_filter = ['id', 'username', 'nickname', 'address', 'telephone']
    search_fields = ['id', 'username', 'nickname', 'address', 'telephone']
    resource_class = UserProfileResource


class EmailVerifyRecordAdmin(ImportExportModelAdmin):
    list_display = ('email', 'send_type', 'send_time', 'code')
    search_fields = ['email', 'send_type', 'send_time', 'code']
    resource_class = VerifyRecordResource


# 注册模型
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

# admin界面设置
# 页面标题
admin.site.site_header = "后台管理系统"
# 标签栏标题
admin.site.site_title = "后台管理系统"
