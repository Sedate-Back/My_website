from django.db import models


# Create your models here.
class Team(models.Model):
    "”“ 团队表 """
    title = models.CharField(verbose_name='团队', max_length=32)

    def __str__(self):
        return self.title


class Userinfo(models.Model):
    """ 会员表 """
    name = models.CharField(verbose_name='姓名', max_length=16)
    job = models.CharField(verbose_name='职位', max_length=16)
    email = models.EmailField(verbose_name="Github邮箱", max_length=64)
    password = models.CharField(verbose_name="账号密码", max_length=32)
    message = models.TextField(verbose_name="信息补充")
    depart = models.ForeignKey(to='Team', to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.name, self.job, self.email, self.message, self.depart, self.password


class Task(models.Model):
    "”“ 任务表 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "重要且紧急"),
        (4, "可以展缓"),
        (5, "待定义")
    )
    level = models.SmallIntegerField(verbose_name="任务等级", choices=level_choices, default=5)
    title = models.CharField(verbose_name="任务名称", max_length=64)
    detail = models.TextField(verbose_name="任务细节")
    name = models.ForeignKey(verbose_name="任务人", to=Userinfo, to_field='id', on_delete=models.CASCADE)
    status_choices = (
        (1, "待开发"),
        (2, "正在开发"),
        (3, "开发完成，测试中"),
        (4, "修改bug中"),
        (5, "完成")
    )
    status = models.SmallIntegerField(verbose_name="任务进行状态", choices=status_choices, default=1)

    def __str__(self):
        return self.title, self.level, self.detail, self.name, self.status


class Content(models.Model):
    """  个人内容表"""
    name = models.ForeignKey(verbose_name="作者/Author", to=Userinfo, to_field="id", on_delete=models.CASCADE)
    time = models.TimeField(verbose_name="创造时间/Create time")
    content = models.CharField(verbose_name="创作内容/Create Content", max_length=5000)

    def __str__(self):
        return self.name, self.time, self.content

