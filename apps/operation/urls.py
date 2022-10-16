# -*- coding: utf-8 -*-

from django.urls import path

from apps.operation.views import AddUserAskView, AddUserFavouriteView, AddCommentsView, DeleteCommentsView

app_name = 'apps.operation'
urlpatterns = [
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),
    path('add_fav/', AddUserFavouriteView.as_view(), name="add_fav"),
    path('add_comments/', AddCommentsView.as_view(), name='add_comments'),
    path('del_comments/', DeleteCommentsView.as_view(), name='del_comments'),
]
