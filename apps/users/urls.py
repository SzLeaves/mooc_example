# -*- coding: utf-8 -*-

from django.urls import path, re_path

from apps.users.views import ActiveUserView, LoginView, LogoutView, RegisterView, ForgetPasswordView, ResetPasswordView
from apps.users.views import MyCoursesView, MyFavouriteView, MyMessagesView, MyMessagesContentView
from apps.users.views import UserInfoView, UploadImageView, ResetPasswordInfoView, UpdateEmailView

app_name = 'apps.users'
urlpatterns = [
    # 登录/注销
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # 注册
    path('register/', RegisterView.as_view(), name="register"),
    re_path('active/(?P<verify_code>.*)/', ActiveUserView.as_view(), name="user_acitve"),
    # 找回密码
    path('forgetpwd/', ForgetPasswordView.as_view(), name="find_password"),
    re_path('forget/(?P<verify_code>.*)/', ResetPasswordView.as_view(), name="reset_password"),

    # 用户个人信息界面/保存修改信息
    path('info/', UserInfoView.as_view(), name="user_info"),
    # 用户修改密码
    path('resetpwd/', ResetPasswordInfoView.as_view(), name='reset_info_password'),
    # 用户修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    # 用户上传头像
    path('upload_image/', UploadImageView.as_view(), name='upload_image'),

    # 用户学习课程
    path('mycourses/', MyCoursesView.as_view(), name='my_courses'),
    # 用户收藏
    re_path('myfav/(?P<types>.*)/', MyFavouriteView.as_view(), name="my_favourite"),
    # 用户消息
    path('messages/', MyMessagesView.as_view(), name='my_messages'),
    # 消息内容
    re_path('content/(?P<msg_id>.*)/', MyMessagesContentView.as_view(), name="msg_content"),
]
