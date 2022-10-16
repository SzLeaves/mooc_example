# -*- coding: utf-8 -*-

from django.shortcuts import render


# 全局403处理
def page_permission_denied(request, exception=403):
    response = render(request, '403_csrf.html')
    response.status_code = 403
    return response


# 全局404处理
def page_not_found(request, exception=404):
    response = render(request, '404.html')
    response.status_code = 404
    return response


# 全局500处理
def page_error(request, exception=500):
    response = render(request, '500.html')
    response.status_code = 500
    return response
