# Generated by Django 4.1 on 2022-11-16 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="password",
            field=models.CharField(max_length=32, verbose_name="账号密码"),
        ),
    ]
