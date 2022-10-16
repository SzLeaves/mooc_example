# -*- coding: utf-8 -*-

from django.urls import path, re_path

from apps.courses.views import CoursesListView, CoursesDetailView, CoursesCommentsView
from apps.courses.views import CoursesVideosView, CoursesPlayView

app_name = 'apps.courses'
urlpatterns = [
    path('list/', CoursesListView.as_view(), name="list"),
    re_path('detail/(?P<course_id>.*)/', CoursesDetailView.as_view(), name="course_detail"),
    re_path('videos/(?P<course_id>.*)/', CoursesVideosView.as_view(), name="course_videos"),
    re_path('comments/(?P<course_id>.*)/', CoursesCommentsView.as_view(), name="course_comments"),
    re_path('play/(?P<video_id>.*)/', CoursesPlayView.as_view(), name="course_play"),
]
