#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
app_name = "task_manage"
from django.urls import path
from django.contrib.auth.decorators import login_required
from task_manage import views

urlpatterns = [
    path('webssh_login/', login_required(views.WebsshLogin.as_view()), name="webssh_login"),
    path('get_env_by_system_id/', views.get_env_by_system_id, name="get_env_by_system_id"),
    path('get_host_by_sys_or_env_id/', views.get_host_by_sys_or_env_id, name="get_host_by_sys_or_env_id"),
    path('get_host_login_user_info_by_id/', views.get_host_login_user_info_by_id, name="get_host_login_user_info_by_id"),
    path('run_cmd/', login_required(views.RunCmd.as_view()), name="run_cmd"),
    path('tail_log/', login_required(views.TailLog.as_view()), name="tail_log"),
    path('tail_stop/', login_required(views.TailStop.as_view()), name="tail_stop"),
    # 方便测试人员查看日志的页面
    path('tester_tail_log/', login_required(views.TesterTailLog.as_view()), name="tester_tail_log"),
    path('tester_tail_stop/', login_required(views.TesterTailStop.as_view()), name="tester_tail_stop"),
    path('get_application_by_ip/', views.get_application_by_ip, name="get_application_by_ip"),
    # 配置免密登录
    path('no_password_to_login/', login_required(views.NoPasswordToLogin.as_view()), name="no_password_to_login"),
    path('test_no_password/', login_required(views.TestNoPassword.as_view()), name="test_no_password"),
    # 服务管理，启动服务或停止服务
    path('manage_server/', login_required(views.ManageServer.as_view()), name="manage_server"),
    path('start_server/', views.start_server, name="start_server"),
    path('restart_server/', views.restart_server, name="restart_server"),
    path('stop_server/', views.stop_server, name="stop_server"),



]
