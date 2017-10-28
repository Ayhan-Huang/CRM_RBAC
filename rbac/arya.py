#! user/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
import json
from arya.service import sites
from . import models
from django import forms
from django.urls import RegexURLPattern
from django.utils.safestring import mark_safe


def get_all_urls(patterns, pre_fix, is_firt_time=False, result=[]):
    if is_firt_time:
        result.clear()

    for item in patterns:
        part = item._regex.strip('^$')
        if isinstance(item, RegexURLPattern):
            val= pre_fix + part
            result.append((val, val))  # 这里改为元组，作为权限下拉选项choice的数据源
        else:
            get_all_urls(item.urlconf_name, pre_fix + part)

    return result


class PermissionModelForm(forms.ModelForm):
    # 重写url字段，使成为下拉框
    url = forms.fields.ChoiceField()

    class Meta:
        fields = '__all__'
        model = models.Permission

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 记住这个不能在顶部导入，因为那时还未注册路由
        from CRM_PRAC.urls import urlpatterns
        # 每次实例化，动态获取字段的值；（否则无法显示新增数据，除非程序重启）
        self.fields['url'].choices = get_all_urls(patterns=urlpatterns, pre_fix='/', is_firt_time=True)


class PermissionConfig(sites.AryaConfig):

    def show_func(self, obj=None, is_header=False):
        if is_header:
            return '自定义表头'
        else:
            return '%s-%s'% (obj.title, obj.url)

    list_display = ['title', 'url','menu', show_func]

    model_form = PermissionModelForm

    # def add_view(self, request, *args, **kwargs):
    # 通过重写add_view方法，在页面显示所有url以供选择
    #
    #     from CRM_PRAC.urls import urlpatterns
    #     # 记住这个不能在顶部导入，因为那时还未注册路由
    #
    #     result = self.get_all_urls(urlpatterns, pre_fix='/', is_firt_time=True)
    #
    #     model_form_cls = self.get_model_form_class()
    #     popup_id = request.GET.get(self.popup_key)
    #     if request.method == 'GET':
    #         form = model_form_cls()
    #
    #         context = {
    #             'form': form,
    #             'url_list': result
    #         }
    #         return render(request, "arya/add_popup_custom.html" if popup_id else "arya/add_custom.html", context)
    #
    #     elif request.method == "POST":
    #         form = model_form_cls(data=request.POST, files=request.FILES)
    #         if form.is_valid():
    #             obj = self.save(form, True)
    #             if obj:
    #                 if popup_id:
    #                     context = {'pk': obj.pk, 'value': str(obj), 'popup_id': popup_id}
    #                     return render(request, 'arya/popup_response.html', {"popup_response_data": json.dumps(context)})
    #                 else:
    #                     return redirect(self.changelist_url_params)
    #         # return render(request, "arya/add_popup_custom.html" if popup_id else "arya/add_custom.html", {'form': form})


class MenuConfig(sites.AryaConfig):
    list_display = ['title', 'parent']


class RoleConfig(sites.AryaConfig):
    def show_permission(self, obj=None, is_header=False):
        if is_header:
            return '权限'
        list = []
        for item in obj.permissions.all():
            tpl = "<span style='margin:2px'>{title}</span>".format(title=item.title)
            list.append(tpl)
        return mark_safe(''.join(list))

    list_display = ['title', show_permission]


class UserInfoConfig(sites.AryaConfig):

    def show_role(self, obj=None, is_header=False):
        # 显示M2M字段，由于字段在第三张表，无法在当前表获取，需要自定义函数，进行跨表查询
        if is_header:
            return '角色'

        roles = obj.roles.all() # 跨表
        list = []
        for role in roles:
            tpl = '<span style="margin: 2px">{title}</span>'.format(title=role.title)
            list.append(tpl)
        return mark_safe(''.join(list))

    list_display = ['username','password', 'email', show_role]


sites.site.register(models.Menu, MenuConfig)
sites.site.register(models.Permission, PermissionConfig)
sites.site.register(models.Role, RoleConfig)
sites.site.register(models.User, UserInfoConfig)

