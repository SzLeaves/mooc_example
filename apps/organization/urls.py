# -*- coding: utf-8 -*-

from django.urls import path, re_path

from apps.organization.views import OrganizationCoursesView, OrganizationDescirbeView
from apps.organization.views import OrganizationTeacherView, TeacherListView, TeacherInfoView
from apps.organization.views import OrganizationView, OrganizationHomeView

app_name = 'apps.organization'
urlpatterns = [
    path('list/', OrganizationView.as_view(), name="list"),
    path('teachers_list/', TeacherListView.as_view(), name="list_teachers"),
    re_path('home/(?P<org_id>.*)/', OrganizationHomeView.as_view(), name="home"),
    re_path('courses/(?P<org_id>.*)/', OrganizationCoursesView.as_view(), name="courses"),
    re_path('desc/(?P<org_id>.*)/', OrganizationDescirbeView.as_view(), name="desc"),
    re_path('teachers/(?P<org_id>.*)/', OrganizationTeacherView.as_view(), name="teachers"),
    re_path('teachers_info/(?P<teacher_id>.*)/', TeacherInfoView.as_view(), name="teachers_info"),
]
