from django.shortcuts import render, redirect
from app01 import models
from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets as wid
from collections import Counter
from app01.utitls.encrypt import md5
from app01.utitls.bootstrap import BootStrapModelForm


# 个人内容视图函数
def content_list(request):
    data = models.Content.objects.all()
    return render(request, "content_list.html", {"data": data})


def content_add(request):
    if request.method == "GET":
        dict_content = {
            'name': models.Userinfo.objects.all(),
        }
        return render(request, "content_add.html", dict_content)
    name_id = request.POST.get('name_id')
    time = request.POST.get("time")
    content = request.POST.get("content")

    models.Content.objects.create(name_id=name_id, time=time, content=content)
    return redirect('/content/list/')

