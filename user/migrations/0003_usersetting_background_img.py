# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-14 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20160513_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='background_img',
            field=models.ImageField(blank=True, upload_to='users/background/%Y/%m/%d', verbose_name='主页背景'),
        ),
    ]
