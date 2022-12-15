"""My_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views, account

urlpatterns = [
    # path("admin/", admin.site.urls),
    #  团队url
    path('team/list/', views.team_list),
    path('team/add/', views.team_add),
    path("team/delete/", views.team_delete),
    path("team/<int:nid>/edit/", views.team_edit),
    # 用户信息url
    path('userinfo/list/', views.userinfo_list),
    path('userinfo/add/', views.userinfo_add),
    # path('userinfo/check', views.userinfo_check),
    path("userinfo/delete/", views.userinfo_delete),
    path("userinfo/<int:nid>/edit/", views.userinfo_edit),

    # 任务列表url
    path('task/list/', views.task_list),
    path('task/add/', views.task_add),
    path("task/delete/", views.task_delete),
    path('task/<int:nid>/edit/', views.task_edit),
    # path('task/add/model/', views.task_model_add),

    # 登录页面
    path("login/", account.login),
    path("logout/", account.logout),
    path("image/code/", account.image_code),

    # 首页
    path("index/", account.index),

    # 个人内容页
    path("userinfo/index/", account.index_userinfo)
]
