# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-14 08:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': '帖子', 'verbose_name_plural': '帖子'},
        ),
    ]
