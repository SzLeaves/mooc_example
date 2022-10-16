# -*- coding: utf-8 -*-

from captcha.fields import CaptchaField
from django import forms

from apps.users.models import UserProfile


class LoginForm(forms.Form):
    # 变量名必须与html字段名一致
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invaild": "验证码错误"})


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invaild": "验证码错误"})


class ResetPasswordForm(forms.Form):
    password_1 = forms.CharField(required=True, min_length=5)
    password_2 = forms.CharField(required=True, min_length=5)


class UpdatePersonalInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'birthday', 'gender', 'address', 'telephone']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
