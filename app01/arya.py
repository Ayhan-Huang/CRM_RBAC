#! user/bin/env python
# -*- coding: utf-8 -*-

from arya.service import sites
from . import models


class UserInfoConfig(sites.AryaConfig):
    list_display = ['id','name', 'username', 'email', 'depart']

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

        # sites.FilterOption('name', is_multi=False),
        sites.FilterOption(filter_func, False,text_func_name=lambda obj: obj.email)
    ]

    """ 如果list_filter如上配置，那么url ? 参数如下：
     depart=4&filter_func=2
    """


class DepartmentConfig(sites.AryaConfig):
    list_display = ['title']

    list_filter = [
        sites.FilterOption('title')
    ]

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
    def extra_urls(self):
        from django.conf.urls import url

        app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name

        patterns = [
            url(r'^detail/$', self.detail_view, name="%s_%s_detail_view" % app_model_name),
        ]
        return patterns

    def detail_view(self,request):
        from django.shortcuts import HttpResponse
        return HttpResponse('详细信息')


class ClassListConfig(sites.AryaConfig):
    def display_func(self):
        pass

    list_display = ['school', 'course', 'semester', 'price', 'start_date', 'graduate_date', 'teachers']

    list_filter = [
        sites.FilterOption('school'),
        sites.FilterOption('course'),
        sites.FilterOption('teachers')
    ]

    def get_show_add_btn(self):
        return False

    def act_func(self):
        pass

    act_func.short_description = '未知功能'

    actions = [act_func]

    def extra_urls(self):
        from django.conf.urls import url

        app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name

        patterns = [
            url(r'^test/$', self.test, name="%s_%s_test" % app_model_name),
        ]

        return patterns

    def test(self, request):
        from django.shortcuts import HttpResponse
        return HttpResponse('TEST....')

sites.site.register(models.UserInfo, UserInfoConfig)
sites.site.register(models.Department, DepartmentConfig)
sites.site.register(models.Course, CourseConfig)
sites.site.register(models.ClassList, ClassListConfig)





