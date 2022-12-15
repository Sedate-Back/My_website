from django.shortcuts import render, HttpResponse, redirect
from django import forms

from app01 import models
from app01.utitls.encrypt import md5
from app01.utitls.code import check_code
from io import BytesIO  # 将生成在内存中的图片给浏览器读取


class LoginForm(forms.Form):
    """ 定义登录的Form组件，相比较modelfor，需要自己来写展示的字段和添加的样式 """
    name = forms.CharField(label="用户名",
                           widget=forms.TextInput(attrs={"class": "form-control"}),
                           required=True)
    # label是字段名， widget是添加的输入框样式， attrs是加入css样式, required 要求必填

    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={"class": "form-control"}),
                               required=True)

    code = forms.CharField(label="验证码",
                           widget=forms.TextInput,
                           required=True)

    """ 定义钩子方法 """

    def clean_password(self):
        """ 把在登录页面输入的密码，拿到后用md5的方式加密，并返回 """
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """ 定义登录页面 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        """ 添加校验，获取到用户输入的用户名和密码（字典的形式），因为上面form里有name、password、code，所以form里就有三个信息在字典里"""
        #  {'username': 'admin', 'password': 'admin', "code": "xxxx"}
        # print("form.cleaned_data：", form.cleaned_data)

        # 验证码的校验
        # 因为下面数据库存储的没有code这个列，所以没办法去校验，得把输入的code删除，就用pop
        user_input_code = form.cleaned_data.pop("code")
        # code的正确答案就是image_code
        code_tru = request.session.get("image_code", "")
        if code_tru.upper() != user_input_code.upper():  # 用户输入和答案转化成大写去比较
            # 不相等就报错
            form.add_error("code", "Code input error, please input again! ")
            return render(request, "login.html", {"form": form})

        # 密码和用户名校验
        # md5 加密后 pwd就变成加密后的样子了  {'name': 'admin', 'password': '0e48218b411921d59d1c250ca9e679de'}；
        # 方法1：
        # admin_obj = models.Userinfo.objects.filter(name=form.cleaned_data["name"],
        # password=form.cleaned_data["password"])
        # 方法2：
        """ 用**form.cleaned_data 的方式，需要确保前端的字段定义和数据库的是否一致 """
        admin_obj = models.Userinfo.objects.filter(**form.cleaned_data).first()
        if not admin_obj:  # 如果账号或密码输入错误（去数据库校验失败的话）
            #  主动添加告警信息，返回给用户
            form.add_error("password", "name or password error, please sure your input message! ")
            return render(request, "login.html", {"form": form})
        # 校验成功后，把用户的信息写到session中
        request.session["info"] = {"name": admin_obj.name}
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/index/")
    return render(request, "login.html", {"form": form})


def image_code(request):
    img, code_string = check_code()  # code_string 就是答案， 需要和用户输入的进行校验
    request.session["image_code"] = code_string
    request.session.set_expiry(60)  # 给session设置60s超时 防止验证码一直有效

    stream = BytesIO()
    img.save(stream, "png")

    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销"""
    request.session.clear()
    return redirect("/login/")


def index(request):
    form = LoginForm(data=request.POST)
    return render(request, "index.html", {"form": form})


def index_userinfo(request):
    form = LoginForm(data=request.POST)
    return render(request, "userinfo_index.html", {"form": form})