from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

"""
此文件为中间件，可以在用户访问系统的时候校验用户有没有登录
没有登录就强制返回登陆页面
info_dict是一个字典，返回的是{name：用户登录名}
需要在settings文件中的中间件加入这个文件的路径 
"""


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        #   request.path_info 获取当前用户请求的URL 如果访问登录页面，path_info= /login/
        if request.path_info in ["/login/", "/image/code/", "/logon/"]:
            return

        # 1.读取当前访问的用户的session信息，如果能读到，说明已登陆过，就可以继续向后走。
        info_dict = request.session.get("info")
        print(info_dict)
        if info_dict:
            return

        # 2.没有登录过，重新回到登录页面
        return redirect('/login/')