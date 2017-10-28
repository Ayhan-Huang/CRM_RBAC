#! user/bin/env python
# -*- coding: utf-8 -*-

from arya.service import sites
from . import models
from django.utils.safestring import mark_safe
from django.db.models import Q



class UserInfoConfig(sites.AryaConfig):
    list_display = ['name', 'depart']

    # 如果FilterOption接收函数，那么该函数必须返回FilterRow对象
    # FilterRow(self, option, change_list, data_list, request)
    # if option.is_func:
    #     data_list = option.field_or_func(self.model_config, option, self)
    def filter_func(self, option, change_list, request):  # self 就是model_config; option, change_list 在gen_list_filter中传递
        data_list = self.model_class.objects.filter(id__gt=1) # data_list 必须手动提供
        return sites.FilterRow(option, change_list, data_list, request)

    list_filter = [
        sites.FilterOption(field_or_func='depart',
                           is_multi=True,
                           text_func_name=lambda obj: obj.title, # 定义筛选a标签的文本
                           val_func_name=lambda obj: obj.id), # url上要传递的值

        sites.FilterOption(filter_func, False,text_func_name=lambda obj: obj.name)
    ]

    """ 如果list_filter如上配置，那么url ? 参数如下：
     depart=4&filter_func=2
    """


class DepartmentConfig(sites.AryaConfig):
    list_display = ['id', 'title']

    # 定制增加按钮
    def get_show_add_btn(self):
        return False

    # 定义actions
    def act_func(self):
        pass

    act_func.short_description = '测试功能'

    actions = [act_func]


class CourseConfig(sites.AryaConfig):
    # 扩展路由
    # def extra_urls(self):
    #     from django.conf.urls import url
    #
    #     app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
    #
    #     patterns = [
    #         url(r'^detail/$', self.detail_view, name="%s_%s_detail_view" % app_model_name),
    #     ]
    #     return patterns
    #
    # def detail_view(self,request):
    #     from django.shortcuts import HttpResponse
    #     return HttpResponse('详细信息')

    list_display = ['name']


class ClassListConfig(sites.AryaConfig):
    def course_semester(self, obj=None, is_header=False):
        # 自定义表头
        if is_header:
            return '课程'
        tpl = '{course}-{semester}期'.format(course=obj.course.name, semester=obj.semester)
        return tpl

    def show_teachers(self, obj=None, is_header=False):
        # 定义M2M字段显示
        if is_header:
            return '任课教师'
        list = []
        for item in obj.teachers.all():
            tpl = "<span style='margin: 2px'>{name}</span>".format(name=item.name)
            list.append(tpl)
        return mark_safe(''.join(list))

    list_display = ['school', course_semester, show_teachers]

    list_filter = [
        sites.FilterOption('school'),
        sites.FilterOption('teachers')
    ]


    def act_func(self):
        pass

    act_func.short_description = '未知功能'

    actions = [act_func]


class CustomerConfig(sites.AryaConfig):
    # 定义静态字段的显示
    def show_education(self, obj=None, is_header=False):
        if is_header:
            return '学历'
        return obj.get_education_display()

    def show_gender(self, obj=None, is_header=False):
        if is_header:
            return '性别'
        return obj.get_gender_display()

    def show_experience(self, obj=None, is_header=False):
        if is_header:
            return '工作经验'
        return obj.get_experience_display

    def show_records(self, obj=None, is_header=False):
        if is_header:
            return '跟进记录'
        # 取出反向关联表ConsultRecord中的记录
        list = []
        for row in obj.consultrecord_set.all():
            tpl = '<div>{date}: {content}</div>'.format(date=row.date, content=row.note)
            list.append(tpl)
        return mark_safe(''.join(list))

    list_display = ['name', show_gender, show_education, 'consultant', show_records, 'date']

    list_filter = [
        # 定义筛选标签的性别显示：
        # 方式一：定义函数如下；方式二：改源码(看笔记)
        sites.FilterOption('gender', is_multi=True, text_func_name=lambda obj: obj.get_gender_display()),
        sites.FilterOption('consultant',is_multi=True, condition=Q(depart_id=1))
        # Customer中的consultant字段是与UserInfo关联的外键字段, 因此通过consultant就可以取到UserInfo对象
        # UserInfo的中有depart外键（数据库存储为depart_id）
    ]

    list_search = ['name']


class StudentConfig(sites.AryaConfig):
    def show_class_list(self, obj=None, is_header=False):
        if is_header:
            return '已报班级'

        list = []
        for item in obj.class_list.all():
            tpl = "<span style='margin: 2px'>{course_name} {semester}期</span>"\
                .format(course_name= item.course.name, semester=item.semester)
            list.append(tpl)
        return mark_safe(''.join(list))

    list_display = [ 'username', show_class_list, 'company']


class SchoolConfig(sites.AryaConfig):
    list_display = ['title']


class ConsultRecordConfig(sites.AryaConfig):
    list_display =['customer', 'consultant', 'date', 'note']


class CourseRecordConfig(sites.AryaConfig):
    list_display = ['course', 'day_num', 'teacher', 'date', 'course_title']

    def init_study_record(self, request):
        """
        根据上课记录，初始化学生学习记录
        上课记录信息：course_record字段，student字段
        判断是否已经生成学习记录，以免重复创建
        :param request: 获取form提交过来的上课记录id
        :return: 
        """
        # 获取上课记录id
        pk_list = request.POST.getlist('pk')
        course_record_list = self.model_class.objects.filter(pk__in=pk_list) # 上课记录列表

        for course_obj in course_record_list:
            # 上课记录 正向--》 班级 反向--》 学生
            current_course_students = course_obj.course.student_set.all() # 当前上课记录Id对应的所有学生

            study_record_list = []
            for student in current_course_students: # 循环当前上课学生，创建记录
                record = models.StudyRecord(course_record=course_obj, student=student)
                study_record_list.append(record)

            models.StudyRecord.objects.bulk_create(study_record_list)

    init_study_record.short_description = '初始化学生学习记录'

    actions = [init_study_record]


class StudyRecordConfig(sites.AryaConfig):
    def show_attend(self, obj=None, is_header=False):
        if is_header:
            return '考勤'
        return obj.get_record_display()

    def show_course(self, obj=None, is_header=False):
        # 显示课程名称
        if is_header:
            return '课程名'

        class_obj = obj.course_record.course
        course_name = class_obj.course.name
        semester = class_obj.semester

        tpl = '<span style="margin: 2px">{0} {1}</span>'.format(course_name, semester)
        return mark_safe(tpl)

    list_display = ['course_record', 'student', show_attend, ]

sites.site.register(models.UserInfo, UserInfoConfig)
sites.site.register(models.Department, DepartmentConfig)
sites.site.register(models.Course, CourseConfig)
sites.site.register(models.ClassList, ClassListConfig)
sites.site.register(models.Customer, CustomerConfig)
sites.site.register(models.Student, StudentConfig)
sites.site.register(models.School, SchoolConfig)
sites.site.register(models.ConsultRecord, ConsultRecordConfig)
sites.site.register(models.CourseRecord, CourseRecordConfig)
sites.site.register(models.StudyRecord, StudyRecordConfig)





