from django.http import HttpResponse
from django.views import View

from apps.courses.models import Courses
from apps.operation.models import UserFavourite, UserCoursesComments
from apps.organization.forms import UserAskForm
from apps.organization.models import CourseOrganization, Teacher


# 用户咨询
class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            # 返回json内容（ajax）
            return HttpResponse('{"status":"success","msg":"提交成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"提交失败"}', content_type='application/json')


# 用户收藏
class AddUserFavouriteView(View):
    def post(self, request):
        # 接收ajax参数
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))

        # 判断用户登录状态
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        # 查询UserFavourite表记录，如果没有记录就添加
        exist_records = UserFavourite.objects.filter(user=request.user, favourite_id=fav_id,
                                                     favourite_type=fav_type)
        if exist_records:
            # 如果记录存在，说明用户需要取消收藏
            exist_records.delete()

            # 使收藏对象的收藏数量-1
            fav_target = None
            if fav_type == 1:
                fav_target = Courses.objects.get(id=fav_id)
            elif fav_type == 2:
                fav_target = CourseOrganization.objects.get(id=fav_id)
            elif fav_type == 3:
                fav_target = Teacher.objects.get(id=fav_id)

            fav_target.favourite_num -= 1
            fav_target.save()

            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')

        else:
            user_fav = UserFavourite()
            # 如果为0默认值说明没有正确取值
            if int(fav_id) > 0 and int(fav_type):
                user_fav.user = request.user
                user_fav.favourite_id = int(fav_id)
                user_fav.favourite_type = int(fav_type)
                user_fav.save()

                # 使收藏对象的收藏数量+1
                fav_target = None
                if fav_type == 1:
                    fav_target = Courses.objects.get(id=fav_id)
                elif fav_type == 2:
                    fav_target = CourseOrganization.objects.get(id=fav_id)
                elif fav_type == 3:
                    fav_target = Teacher.objects.get(id=fav_id)

                fav_target.favourite_num += 1
                fav_target.save()

                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏失败"}', content_type='application/json')


# 用户评论
class AddCommentsView(View):
    def post(self, request):
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = int(request.POST.get('course_id'))
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            user_comments = UserCoursesComments()
            # 用户评论课程
            user_comments.course = Courses.objects.get(id=int(course_id))
            # 评论的用户
            user_comments.user = request.user
            # 评论信息
            user_comments.comments = comments

            # 保存信息
            user_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')


# 删除用户评论
class DeleteCommentsView(View):
    def post(self, request):
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        comment_id = int(request.POST.get('comment_id', ''))
        if comment_id > 0:
            try:
                del_comment = UserCoursesComments.objects.get(id=comment_id)
                # 判断是否为用户本人操作
                if request.user.id == del_comment.user.id:
                    del_comment.delete()
                    return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
            except Exception:
                pass

        return HttpResponse('{"status":"fail","msg":"删除失败"}', content_type='application/json')
