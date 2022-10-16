from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

import mooc_example.exception
from apps.users.views import IndexView
from mooc_example.settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    # 后台管理
    path('admin/', admin.site.urls),

    # 主页
    path('', IndexView.as_view(), name='index'),
    path('index/', IndexView.as_view(), name='index'),

    # 用户登录
    path('users/', include('apps.users.urls', namespace='users')),

    # 用户操作
    path('operation/', include('apps.operation.urls', namespace='operations')),

    # 课程机构
    path('orgs/', include('apps.organization.urls', namespace='orgs')),

    # 公开课
    path('courses/', include('apps.courses.urls', namespace='courses')),

    # 验证码
    path('captcha/', include('captcha.urls')),

    # 上传图片
    re_path('^upload/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # 静态文件
    re_path('^static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
]

# 全局错误页面
handler403 = mooc_example.exception.page_permission_denied
handler404 = mooc_example.exception.page_not_found
handler500 = mooc_example.exception.page_error
