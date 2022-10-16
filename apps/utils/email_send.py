# -*- coding: utf-8 -*-

import random

from django.core.mail import send_mail

from apps.users.models import EmailVerifyRecord
from mooc_example.settings import EMAIL_HOST_USER


def send_register_email(email, send_type='register'):
    # 创建验证码对象
    email_record = EmailVerifyRecord()

    # 生成验证码
    if send_type == 'update':
        # 重新绑定邮箱验证码使用4位，方便填写
        email_record.code = generate_random_str()[:4]
    else:
        email_record.code = generate_random_str()

    email_record.email = email
    email_record.send_type = send_type
    # 存入数据库，后面需要查询
    email_record.save()

    # 发送邮件
    if send_type == 'register':
        email_title = "在线注册激活链接"
        email_body = "请点击链接激活帐号：http://127.0.0.1:8000/users/active/%s" % email_record.code
        send_mail(email_title, email_body, EMAIL_HOST_USER, [email])

    elif send_type == 'forget':
        email_title = "找回密码链接"
        email_body = "请点击链接找回帐号密码：http://127.0.0.1:8000/users/forget/%s" % email_record.code
        send_mail(email_title, email_body, EMAIL_HOST_USER, [email])

    elif send_type == 'update':
        email_title = "重置邮箱绑定链接"
        email_body = "你的新邮箱绑定验证码：%s" % email_record.code
        send_mail(email_title, email_body, EMAIL_HOST_USER, [email])


# 生成验证码
def generate_random_str():
    random_string = ''
    charset = ''.join([chr(i) for i in range(65, 65 + 26)] +
                      [chr(i) for i in range(97, 97 + 26)] +
                      [str(i) for i in range(10)])

    for ch in range(len(charset)):
        random_string += charset[random.randint(0, len(charset) - 1)]

    return random_string[:20]
