# -*- coding: utf-8 -*-

import re

from django import forms

from apps.operation.models import UserAsk


# 使用ModelForm继承已有Model配置，转换为新的Form
class UserAskForm(forms.ModelForm):
    # 也可以跟常规的Form一样添加字段，并且继承了Model的属性
    user = forms.CharField(min_length=2)
    course_name = forms.CharField(max_length=20)

    class Meta:
        # 指定转换的Model
        model = UserAsk
        # 指定需要转换的字段
        fields = ['user', 'telephone', 'course_name']

    # 重写clean方法自定义验证
    def clean(self):
        telephone = self.cleaned_data['telephone']
        regex = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(regex)
        if not telephone or not p.match(telephone):
            raise forms.ValidationError("手机号码不正确", code="phone_invaild")
