# -*- coding: utf-8 -*-

from import_export import resources

from apps.operation.models import UserAsk
from apps.operation.models import UserCourses
from apps.operation.models import UserCoursesComments
from apps.operation.models import UserFavourite
from apps.operation.models import UserMessage


class UserAskResource(resources.ModelResource):
    class Meta:
        model = UserAsk


class UserFavouriteResource(resources.ModelResource):
    class Meta:
        model = UserFavourite


class UserMessageResource(resources.ModelResource):
    class Meta:
        model = UserMessage


class UserCoursesResource(resources.ModelResource):
    class Meta:
        model = UserCourses


class UserCoursesCommentsResource(resources.ModelResource):
    class Meta:
        model = UserCoursesComments
