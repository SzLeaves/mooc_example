# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.operation.models import UserFavourite
from apps.organization.models import CourseOrganization, CityList, Teacher


class OrganizationView(View):
    # 课程机构列表功能
    def get(self, request):
        all_orgs = CourseOrganization.objects.all()
        all_cities = CityList.objects.all()
        hot_orgs = all_orgs.order_by("-click_num")[:3]
        all_orgs_num = all_orgs.count()

        # 计算各个机构的课程数量
        for org in all_orgs:
            org.courses_num = org.courses_set.all().count()
            org.save()

        # 关键词搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keyword) |
                Q(describe__icontains=search_keyword) |
                Q(city__name__icontains=search_keyword)
            )

        # 筛选-城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 筛选-机构
        category = request.GET.get('category', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 筛选-排序
        sort = request.GET.get('sort', "")
        if sort == "students_num":
            all_orgs = all_orgs.order_by('-students_num')
        elif sort == "courses":
            all_orgs = all_orgs.order_by('-courses_num')

        # 筛选后all_orgs只包含符合条件的结果返回给页面 #

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        orgs = Paginator(all_orgs, 4, request=request).page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_cities": all_cities,
            "all_orgs_num": all_orgs_num,
            "hot_orgs": hot_orgs,
            "city_id": city_id,
            "category": category,
            "sort": sort,
            "search_keyword": search_keyword,
        })


# 机构首页
class OrganizationHomeView(View):
    def get(self, request, org_id):
        course_org = CourseOrganization.objects.get(id=int(org_id))
        all_courses = course_org.courses_set.all()[:4]
        all_teachers = course_org.teacher_set.all()[:4]

        has_fav = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, favourite_id=course_org.id):
                has_fav = True

        # 访问机构首页的点击数+1
        course_org.click_num += 1
        course_org.save()

        return render(request, 'org-detail-homepage.html', {
            'org_id': org_id,
            'course_orgs': course_org,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            "has_fav": has_fav,
        })


# 机构课程
class OrganizationCoursesView(View):
    def get(self, request, org_id):
        course_org = CourseOrganization.objects.get(id=int(org_id))
        all_courses = course_org.courses_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, favourite_id=course_org.id):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            "course_orgs": course_org,
            "all_courses": all_courses,
            "org_id": org_id,
            "has_fav": has_fav,
        })


# 机构简介
class OrganizationDescirbeView(View):
    def get(self, request, org_id):
        course_org = CourseOrganization.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, favourite_id=course_org.id):
                has_fav = True

        return render(request, "org-detail-desc.html", {
            "org_id": org_id,
            "course_orgs": course_org,
            "has_fav": has_fav,
        })


# 机构教师页面
class OrganizationTeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrganization.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, favourite_id=course_org.id):
                has_fav = True

        return render(request, "org-detail-teachers.html", {
            "org_id": org_id,
            "course_orgs": course_org,
            "all_teachers": all_teachers,
            "has_fav": has_fav,
        })


# 教师列表页面
class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        teachers_num = teachers.count()
        # 讲师排行榜（取前3）
        hot_teachers = teachers.order_by('-click_num')[:3]

        # 关键词搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            teachers = teachers.filter(
                Q(name__icontains=search_keyword) |
                Q(organization__name__icontains=search_keyword)
            )

        # 筛选-人气排名（收藏数量降序）
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-favourite_num')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        teachers = Paginator(teachers, 4, request=request).page(page)

        return render(request, 'teachers-list.html', {
            "teachers": teachers,
            "teachers_num": teachers_num,
            "hot_teachers": hot_teachers,
            "sort": sort,
            "search_keyword": search_keyword,
        })


# 教师详情页面
class TeacherInfoView(View):
    def get(self, request, teacher_id):
        # 获取当前id教师信息
        teacher = Teacher.objects.get(id=int(teacher_id))
        # 通过外键取出教师的课程
        courses = teacher.courses_set.all()
        # 教师的机构
        org = teacher.organization
        # 讲师排行榜（取前3）
        hot_teachers = Teacher.objects.all().order_by('-click_num')[:3]

        # 获取用户收藏信息
        has_teacher_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, favourite_id=teacher_id, favourite_type=3):
                has_teacher_fav = True
            if UserFavourite.objects.filter(user=request.user, favourite_id=org.id, favourite_type=2):
                has_org_fav = True

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        all_courses = Paginator(courses, 6, request=request).page(page)

        # 访问教师页面点击数+1
        teacher.click_num += 1
        teacher.save()

        return render(request, 'teacher-detail.html', {
            "teacher": teacher,
            "courses": all_courses,
            "courses_num": courses.count(),
            "org": org,
            "hot_teachers": hot_teachers,
            "has_teacher_fav": has_teacher_fav,
            "has_org_fav": has_org_fav,
        })
