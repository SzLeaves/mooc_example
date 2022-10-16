# -*- coding: utf-8 -*-

from import_export import resources

from apps.users.models import EmailVerifyRecord
from apps.users.models import UserProfile


class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile


class VerifyRecordResource(resources.ModelResource):
    class Meta:
        model = EmailVerifyRecord
