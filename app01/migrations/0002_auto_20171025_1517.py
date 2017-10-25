# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-25 07:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=64, null=True, verbose_name='邮箱'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='password',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='密码'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='username',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='depart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Department', verbose_name='部门'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='员工姓名'),
        ),
    ]