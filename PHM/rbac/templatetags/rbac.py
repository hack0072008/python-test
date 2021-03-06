#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import re
from django.template import Library
from collections import OrderedDict
from django.conf import settings
from rbac.service import urls
register = Library()


@register.inclusion_tag("rbac/multi_menu.html")
def multi_menu(request):
    """
    二级菜单
    :param request:
    :return:
    """
    menu_dict = request.session.get(settings.SESSION_MENU_KEY)
    # {1: {'title': '信息管理', 'icon': 'fa-fire', 'children': [{'title': '客户列表', 'url': '/customer/list/'}]},
    #  2: {'title': '用户管理', 'icon': 'fa-fire', 'children': [{'title': '账单列表', 'url': '/payment/list/'}]}}
    # 对字典的key进行排序
    key_list = sorted(menu_dict)
    # 空的有序字典
    ordered_dict = OrderedDict()
    # 这里是二级菜单的显示效果，只展开当前访问的路径的菜单，其余菜单是关闭状态
    # li = [{"tile":"wewe"}]
    # # Create your tests here.
    # li[0]["tile"] = "new"
    # print(li)  # [{'tile': 'new'}]
    # 利用了字典是可变类型，一处修改了，原来的内容也跟着变了
    for key in key_list:
        val = menu_dict[key]
        val['class'] = ""

        for per in val['children']:
            if per['id'] == request.current_selected_permission:
                per['class'] = 'current_active'
                # 父菜单添加active的class
                val['class'] = 'active'
                # 父菜单处于展开状态
                val["expanded"] = "true"
        ordered_dict[key] = val
    #         注意这里的返回值，要是字典，前端直接循环menu_list
    return {
        'menu_dict': request.session.get(settings.SESSION_MENU_KEY)
    }


@register.inclusion_tag("rbac/breadcrumb.html")
def breadcrumb(request):
    # record_list = [{"title": "首页", "url": "#"}, {}, {}]
    return {'record_list': request.breadcrumb}


@register.filter
def has_permission(request, name):
    """
    判断是否有权限
    :param request:
    :param name:
    :return:
    """
    if name in request.session[settings.SESSION_PERMISSION_URL]:
        return True


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name:
    :return:
    """
    return urls.memory_url(request, name, *args, **kwargs)