# -*- coding: utf-8 -*-

from import_export import resources

from apps.organization.models import CityList
from apps.organization.models import CourseOrganization
from apps.organization.models import Teacher


class CityListResource(resources.ModelResource):
    class Meta:
        model = CityList


class CourseOrganizationResource(resources.ModelResource):
    class Meta:
        model = CourseOrganization


class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher
