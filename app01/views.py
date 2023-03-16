from django.shortcuts import render, redirect
from app01 import models
from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets as wid
from collections import Counter
from app01.utitls.encrypt import md5
from app01.utitls.bootstrap import BootStrapModelForm


# Create your views here.

def team_list(request):
    """ 团队表 """
    data = models.Team.objects.all()
    return render(request, "team_list.html", {"data": data})


class TeamModelForm(forms.ModelForm):
    """ 添加团队表的ModelForm"""

    class Meta:
        model = models.Team
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def team_add(request):
    """ 添加团队 """
    if request.method == "GET":
        form = TeamModelForm()
        return render(request, "team_add.html", {"form": form})

    form = TeamModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/team/list/")
    return render(request, "team_add.html", {"form": form})


def team_delete(request):
    """  删除团队 """
    nid = request.GET.get("nid")
    models.Team.objects.filter(id=nid).delete()
    return redirect("/team/list/")


def team_edit(request, nid):
    """ 根据团队id编辑团队 """
    if request.method == "GET":
        row_obj = models.Team.objects.filter(id=nid).first()
        form = TeamModelForm(instance=row_obj)
        return render(request, "team_edit.html", {"form": form})

    title = request.POST.get("title")
    models.Team.objects.filter(id=nid).update(title=title)
    return redirect("/team/list/")


def userinfo_list(request):
    """ 用户表"""
    info = request.session.get("info")
    #  print("info: ", info)  #  {'name': '林耀'}
    if not info:
        return redirect("/login/")

    data = models.Userinfo.objects.all()
    return render(request, "userinfo_list.html", {"data": data})


class UserinfoModelForm(forms.ModelForm):
    """  添加用户的ModelForm """

    class Meta:
        model = models.Userinfo
        fields = ["name", "job", 'email', 'message', 'password', 'depart']
        widgets = {"password": forms.PasswordInput(render_value=True)}  # 加入密码框样式

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def userinfo_add(request):
    """  添加用户 """
    if request.method == "GET":
        # form = UserinfoModelForm()
        dict_user = {
            'depart': models.Team.objects.all()
        }
        return render(request, "userinfo_add.html", dict_user)

    name = request.POST.get("name")
    password = request.POST.get("password")
    depart_id = request.POST.get("depart_id")
    job = request.POST.get("job")
    email = request.POST.get("email")
    message = request.POST.get("message")

    # 加密password
    # 1 获取用户填写的密码
    # 2 用md5 加密 123456 => 728032b419346e034d37f8a135105c6f
    password = md5(password)
    models.Userinfo.objects.create(name=name, password=password, depart_id=depart_id, job=job, email=email, message=message)
    return redirect('/userinfo/list')


def userinfo_delete(request):
    """ 删除用户 """
    nid = request.GET.get("nid")
    models.Userinfo.objects.filter(id=nid).delete()
    return redirect("/userinfo/list/")


def userinfo_edit(request, nid):
    """ 编辑用户信息 """
    if request.method == "GET":
        row_obj = models.Userinfo.objects.filter(id=nid).first()
        print("row_obj.name: ", row_obj.name)
        form = UserinfoModelForm(instance=row_obj)
        return render(request, "userinfo_edit.html", {"form": form})

    form = UserinfoModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据存在，就取出form的数据，进行逻辑处理
        # {'name': 'linyao', 'job': '前端工程师', 'email': 'linyao@qq.com',
        # 'message': '待补充', 'password': '1f9066315a310a154eb32786a2c771bf', 'depart': <Team: 全栈工程师>}
        # 1。 判断用户名是否唯一
        name_obj = models.Userinfo.objects.filter(name=form.cleaned_data["name"])
        #  or form.cleaned_data["name"]== models.Userinfo.objects.filter(id=nid).first().name 未更改名称
        if not name_obj or form.cleaned_data["name"] == models.Userinfo.objects.filter(id=nid).first().name:
            # 如果对象不存在，就可以进行更新数据
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            job = form.cleaned_data["job"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            depart_id = form.cleaned_data["depart"].id
            models.Userinfo.objects.filter(id=nid).update(name=name, password=password,
                                                          job=job, email=email, message=message, depart_id=depart_id)
            return redirect("/userinfo/list/")
        # 如果名称重复了，就报错
        form.add_error("name", "This name is exist! Please try input another one!")
    return render(request, "userinfo_edit.html", {"form": form})


def task_list(request):
    """  任务表 """
    if request.method == "GET":
        data = models.Task.objects.all()
        return render(request, 'task_list.html', {"data": data})
    data = models.Task.objects.all().order_by("status")
    return render(request, 'task_list.html', {"data": data})


def task_add(request):
    """  添加任务表 """
    if request.method == "GET":
        dict_task = {
            'name': models.Userinfo.objects.all(),
            'level_choices': models.Task.level_choices,
            "status_choices": models.Task.status_choices,
        }
        return render(request, "task_add.html", dict_task)
    name_id = request.POST.get('name_id')
    level = request.POST.get('level')
    title = request.POST.get('title')
    detail = request.POST.get('detail')
    status = request.POST.get("status")
    models.Task.objects.create(level=level, name_id=name_id, title=title, detail=detail, status=status)
    return redirect('/task/list')


def task_delete(request):
    """ 删除用户表 """
    nid = request.GET.get("nid")
    models.Task.objects.filter(id=nid).delete()
    return redirect("/task/list/")


def task_edit(request, nid):
    """ 修改任务状态 """
    title = "修改任务状态"
    if request.method == "GET":
        row_obj = models.Task.objects.filter(id=nid).first()
        # form = TaskModelForm(instance=row_obj)
        # print(form.fields)  {'level': <django.forms.fields.TypedChoiceField object at 0x00000147AEE17BB0>,
        # 'title': <django.forms.fields.CharField object at 0x00000147AEE17DC0>, 'detail':
        # <django.forms.fields.CharField object at 0x00000147AEE17220>, 'name': <django.forms.models.ModelChoiceField
        # object at 0x00000147AEE17E20>, 'status': <django.forms.fields.TypedChoiceField object at 0x00000147AEE17160>}
        return render(request, "task_edit.html", {"row_obj": row_obj, "title": title})

    # row_obj = models.Task.objects.filter(id=nid).first()
    # form = TaskModelForm(data=request.POST, instance=row_obj)
    # level = request.POST.get("level")
    # title = request.POST.get("title")
    # detail = request.POST.get("detail")
    # name = request.POST.get("name")
    status = request.POST.get("status")
    # models.Task.objects.filter(id=nid).update(level=level, title=title, detail=detail, name=name, status=status)
    models.Task.objects.filter(id=nid).update(status=status)
    return redirect('/task/list/')


