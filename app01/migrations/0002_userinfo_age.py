# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-27 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='age',
            field=models.CharField(default=1, max_length=32, verbose_name='age'),
        ),
    ]
