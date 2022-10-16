import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Courses, CarouselBanner
from apps.operation.models import UserCourses, UserFavourite, UserMessage
from apps.organization.models import CourseOrganization, Teacher
from apps.users.forms import LoginForm, RegisterForm, ResetPasswordForm, ForgetPasswordForm
from apps.users.forms import UploadImageForm, UpdatePersonalInfoForm
from apps.users.models import UserProfile, EmailVerifyRecord
from apps.utils.email_send import send_register_email
from apps.utils.mixin import LoginRequiredMixin


# 自定义登录逻辑
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 模型数据取并集
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception:
            return None


"""
# 主页界面 #
"""


class IndexView(View):
    def get(self, request):
        # 头部广告位轮播课程
        courses_banner = CarouselBanner.objects.all().order_by('index')
        # 非广告位课程
        courses = Courses.objects.filter(is_carousel=False)[:6]
        # 非广告位轮播课程（按点击量取前3）
        banner_courses = Courses.objects.filter(is_carousel=False).order_by('-click_num')[:3]
        # 机构（按点击量取前15）
        course_orgs = CourseOrganization.objects.all().order_by('-click_num')[:15]

        return render(request, "index.html", {
            "courses_banner": courses_banner,
            "coueses": courses,
            "banner": banner_courses,
            "orgs": course_orgs,
        })


"""
# 用户注册界面操作 #
"""


# 注册界面操作
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 注册流程
            # 获取用户表单数据
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')
            # 新建用户对象保存数据
            new_user = UserProfile()
            new_user.is_active = False
            new_user.username = username
            new_user.email = username
            new_user.password = make_password(password)
            # 查询用户是否存在
            if UserProfile.objects.filter(email=username):
                return render(request, "register.html", {"register_form": register_form, "err_msg": " 用户已存在"})

            # 提交数据库
            new_user.save()
            send_register_email(username, 'register')

            return render(request, "login.html", {"err_msg": "注册成功，请查看邮箱激活账户"})

        else:
            return render(request, "register.html", {"register_form": register_form, "err_msg": "注册失败"})


# 激活用户操作
class ActiveUserView(View):
    def get(self, request, verify_code):
        all_records = EmailVerifyRecord.objects.filter(code=verify_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

                # 使该用户激活id失效
                all_records.delete()

                # 给新注册用户发送欢迎消息
                welcome_msg = UserMessage(user=user)
                welcome_msg.title = '欢迎新用户'
                welcome_msg.content = '欢迎使用本网站学习课程！'
                welcome_msg.save()

                return render(request, "login.html", {"err_msg": "激活成功"})
        else:
            return render(request, "403_csrf.html")


# 登录界面操作
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        """
        不管前端是否验证表单，后端都要做
        用户可能通过绕过js验证通过ajax进行非法访问
        """
        # 表单格式验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 与数据库记录验证
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # 登录成功
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"), {"login_form": login_form})
                else:
                    return render(request, "login.html", {"err_msg": "用户未激活"})
            else:
                return render(request, "login.html", {"err_msg": "用户名或密码错误"})

        return render(request, "login.html", {"err_msg": "用户名或密码错误"})


# 注销用户操作
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


# 找回密码操作
class ForgetPasswordView(View):
    def get(self, request):
        forget_password_form = ForgetPasswordForm()
        return render(request, "forgetpwd.html", {"forgerpwd_form": forget_password_form})

    def post(self, request):
        forget_password_form = ForgetPasswordForm(request.POST)
        email = request.POST.get('email', '')
        is_user_exist = len(UserProfile.objects.filter(username=email, email=email)) == 1
        if forget_password_form.is_valid():
            if is_user_exist:
                send_register_email(email, 'forget')
                return render(request, "login.html", {"err_msg": "重置密码链接已发送"})
            else:
                return render(request, "forgetpwd.html",
                              {"forgerpwd_form": forget_password_form, "err_msg": "帐号不存在"})
        else:
            return render(request, "forgetpwd.html", {"forgerpwd_form": forget_password_form, "err_msg": "请求失败"})


# 重置密码操作
class ResetPasswordView(View):
    email = None

    def get(self, request, verify_code):
        all_records = EmailVerifyRecord.objects.filter(code=verify_code, send_type='forget')
        if all_records:
            for record in all_records:
                ResetPasswordView.email = record.email
                return render(request, "resetpwd.html", {'verify_code': verify_code})
        else:
            return render(request, "403_csrf.html")

    def post(self, request, verify_code):
        all_records = EmailVerifyRecord.objects.filter(code=verify_code, send_type='forget')
        resetpwd_form = ResetPasswordForm(request.POST)
        is_same_password = str(request.POST.get('password_1', '')) == str(request.POST.get('password_2', ''))
        if all_records:
            if resetpwd_form.is_valid():
                if is_same_password:
                    user = UserProfile.objects.get(email=ResetPasswordView.email)
                    user.password = make_password(request.POST.get('password_1', ''))
                    user.save()

                    # 使该用户激活码失效
                    all_records.delete()
                    return render(request, "login.html", {"err_msg": "修改成功，请重新登录"})
                else:
                    return render(request, "resetpwd.html", {"err_msg": "重置失败，两次密码不正确"})
            else:
                return render(request, "resetpwd.html", {"resetpwd_form": resetpwd_form})
        else:
            return render(request, "403_csrf.html")


"""
# 用户个人信息界面操作 #
"""


# 用户个人信息页面
class UserInfoView(LoginRequiredMixin, View):
    # 返回信息修改页面
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    # 提交修改信息
    def post(self, request):
        update_info_form = UpdatePersonalInfoForm(request.POST, instance=request.user)
        if update_info_form.is_valid():
            update_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(update_info_form.errors), content_type='application/json')


# 用户信息界面修改密码
class ResetPasswordInfoView(LoginRequiredMixin, View):
    def post(self, request):
        # 验证表单是否正确
        resetpwd_form = ResetPasswordForm(request.POST)
        # 判断密码是否相同
        is_same_password = str(request.POST.get('password_1', '')) == str(request.POST.get('password_2', ''))
        if resetpwd_form.is_valid():
            if is_same_password:
                user = request.user
                user.password = make_password(request.POST.get('password_1', ''))
                user.save()
                return HttpResponse('{"status":"success","msg":"密码重置成功"}', content_type='application/json')

            else:
                return HttpResponse('{"status":"fail","msg":"重置失败，两次密码不正确"}',
                                    content_type='application/json')
        else:
            # 可以使用表单验证类中的errors信息作为响应结果
            return HttpResponse(json.dumps(resetpwd_form.errors), content_type='application/json')


# 用户修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    # 发送邮件验证码 (GET)
    def get(self, request):
        # 验证邮箱是否已被绑定
        email = request.GET.get('email', '')
        users_email = UserProfile.objects.filter(email=email)
        if users_email:
            return HttpResponse('{"status":"failure"}', content_type='application/json')

        # 发送邮箱验证码
        send_register_email(email, 'update')
        return HttpResponse('{"status":"success"}', content_type='application/json')

    # 验证通过后的表单提交 (POST)
    def post(self, request):
        verify_code = request.POST.get('code', '')
        new_email = request.POST.get('email', '')
        # 查询验证码是否正确
        all_verify_code = EmailVerifyRecord.objects.filter(code=verify_code, send_type='update', email=new_email)
        if all_verify_code:
            # 更新用户邮箱信息
            request.user.email = new_email
            request.user.save()
            # 使验证码失效
            all_verify_code.delete()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure"}', content_type='application/json')


# 用户修改头像
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        # 注意传递request.FILES, 用于保存上传的文件信息
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # form在验证时会将上传的数据保存于内存中, 验证通过后会自动保存于model设置的文件路径中
            # 只需要在Form参数中传递instance指定实例化对象就可以直接保存该字段的修改
            image_form.save()
            # 返回响应数据
            return HttpResponse('{"status":"success"}', content_type='application/json')

        return HttpResponse('{"status":"fail"}', content_type='application/json')


# 用户学习课程
class MyCoursesView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourses.objects.filter(user=request.user)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        user_courses = Paginator(user_courses, 8, request=request).page(page)

        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
        })

    # 取消学习课程
    def post(self, request):
        try:
            course_id = request.POST.get('course_id', '')
            user_record = UserCourses.objects.get(user=request.user, course_id=course_id)
            user_record.delete()

            # 使该课程学习人数-1
            study_course = Courses.objects.get(id=course_id)
            study_course.students_num -= 1
            study_course.save()
            # 使该机构学习人数-1
            study_org = CourseOrganization.objects.get(id=study_course.organization.id)
            study_org.students_num -= 1
            study_org.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        except Exception:
            return HttpResponse('{"status":"failure"}', content_type='application/json')


# 用户收藏
class MyFavouriteView(LoginRequiredMixin, View):
    def get(self, request, types):
        if types == 'org':
            fav_id = [item.favourite_id for item in UserFavourite.objects.filter(user=request.user, favourite_type=2)]
            my_orgs = CourseOrganization.objects.filter(id__in=fav_id)
            return render(request, 'usercenter-fav-org.html', {
                "my_orgs": my_orgs,
            })

        elif types == 'teacher':
            fav_id = [item.favourite_id for item in UserFavourite.objects.filter(user=request.user, favourite_type=3)]
            my_teacher = Teacher.objects.filter(id__in=fav_id)
            return render(request, 'usercenter-fav-teacher.html', {
                "my_teachers": my_teacher,
            })

        elif types == 'courses':
            fav_id = [item.favourite_id for item in UserFavourite.objects.filter(user=request.user, favourite_type=1)]
            my_courses = Courses.objects.filter(id__in=fav_id)
            return render(request, 'usercenter-fav-course.html', {
                "my_courses": my_courses,
            })


# 用户消息
class MyMessagesView(LoginRequiredMixin, View):
    def get(self, request):
        # 获取用户消息
        user_messages = UserMessage.objects.filter(user=request.user)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        user_messages = Paginator(user_messages, 8, request=request).page(page)

        return render(request, "usercenter-message.html", {
            "user_messages": user_messages,
        })


# 用户消息内容
class MyMessagesContentView(LoginRequiredMixin, View):
    def get(self, request, msg_id):
        msg = UserMessage.objects.get(user=request.user, id=msg_id)
        # 改变消息状态
        msg.is_read = True
        msg.save()

        return render(request, "usercenter-message-content.html", {
            "message": msg
        })
