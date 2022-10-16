from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Courses, CourseDownload, Videos
from apps.operation.models import UserFavourite, UserCoursesComments, UserCourses
from apps.utils.mixin import LoginRequiredMixin


# 获取学习过相同课程的用户id
def getSameCourseUsers(course):
    return [item.user.id for item in UserCourses.objects.filter(course=course)]


class CoursesListView(View):
    def get(self, request):
        all_courses = Courses.objects.all()
        # 课程前三点击排名
        hot_courses = Courses.objects.all().order_by("-click_num")[:3]

        # 关键词搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            """
            [var_name]__icontains 等同于SQL的 where like 子句，i表示不区分大小写
            [var_name]__contains 用于区分大小写
            """
            # 搜索课程（注意字段名称），对所有结果取并集操作
            all_courses = all_courses.filter(
                Q(name__icontains=search_keyword) |
                Q(describe=search_keyword) |
                Q(detail=search_keyword) |
                Q(tag=search_keyword) |
                Q(category=search_keyword)
            )

        # 排序
        sort = request.GET.get('sort', 'new')
        if sort == 'new':
            all_courses = all_courses.order_by("-add_time")
        elif sort == 'hot':
            all_courses = all_courses.order_by("-click_num")
        elif sort == 'students':
            all_courses = all_courses.order_by("-students_num")

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        courses = Paginator(all_courses, 6, request=request).page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "hot_courses": hot_courses,
            "sort": sort,
            "search_keyword": search_keyword,
        })


class CoursesDetailView(View):
    def get(self, request, course_id):
        course = Courses.objects.get(id=int(course_id))

        # 查询推荐标签
        relate_tags = list()
        if course.tag:
            relate_tags = Courses.objects.filter(tag=course.tag)[:1]

        # 访问时课程点击数+1
        course.click_num += 1
        course.save()

        # 课程/课程机构收藏
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, favourite_id=course_id, favourite_type=1):
                has_fav_course = True
            if UserFavourite.objects.filter(user=request.user, favourite_id=course.organization.id, favourite_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            "course": course,
            "chapter_num": course.getChapterNumber(),
            "student_info": course.getUserCourses(),
            "teachers_num": course.organization.getTeachersNumber(),
            "relate_tags": relate_tags,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


"""
LoginRequiredMixin用于需要登录才能访问的页面 (utils/mixin.py)
使用时注意继承顺序（从左到右）

使用Mixin方式引入验证机制
宿主类的主体逻辑不会因为去掉Mixin而受到影响
同时也不存在超类方法调用（super）以避免引入 MRO 查找顺序问题
"""


class CoursesVideosView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        # 课程信息
        course = Courses.objects.get(id=int(course_id))
        # 课程资源
        resource = CourseDownload.objects.filter(course=course)
        # 学习过该课程的所有用户（注意如何使用user_id外键查找）
        users_study = UserCourses.objects.filter(user_id__in=getSameCourseUsers(course))
        # 从学习过该课程的用户中取出用户其他的学习课程，按点击量降序排序（注意set去重）
        relate_courses = sorted(set([item.course for item in users_study]),
                                key=lambda x: x.click_num, reverse=True)
        # 从推荐列表删除当前的课程
        if len(relate_courses) != 0:
            relate_courses.remove(course)

        # 查询用户是否关联该课程，没有则加入学习列表
        is_select = UserCourses.objects.filter(user=request.user, course=course)
        if not is_select:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()
            # 使该课程学习人数+1
            course.students_num += 1
            course.save()
            # 使机构学习人数+1
            course.organization.students_num += 1
            course.organization.save()

        return render(request, 'course-video.html', {
            "course": course,
            "chapters": course.getChapter(),
            "resource": resource,
            "relate_courses": relate_courses[:3],  # 取排名前3
        })


class CoursesCommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        # 课程信息
        course = Courses.objects.get(id=int(course_id))
        # 课程资源
        resource = CourseDownload.objects.filter(course=course)
        # 课程评论
        comments = UserCoursesComments.objects.filter(course=course)
        # 学习过该课程的所有用户（注意如何使用user_id外键查找）
        users_study = UserCourses.objects.filter(user_id__in=getSameCourseUsers(course))
        # 从学习过该课程的用户中取出用户其他的学习课程id，按点击量降序排序
        relate_courses = sorted(set([item.course for item in users_study]),
                                key=lambda x: x.click_num, reverse=True)
        # 删除当前的课程
        relate_courses.remove(course)

        return render(request, 'course-comment.html', {
            "course": course,
            "resource": resource,
            "comments": comments,
            "relate_courses": relate_courses[:3],  # 取排名前3
        })


class CoursesPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        # 视频信息
        video = Videos.objects.get(id=int(video_id))
        # 课程信息
        course = video.lesson.course
        # 课程资源
        resource = CourseDownload.objects.filter(course=course)

        return render(request, 'course-play.html', {
            "course": course,
            "chapters": course.getChapter(),
            "resource": resource,
            "video": video,
        })
