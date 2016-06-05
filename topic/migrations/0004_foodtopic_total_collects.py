# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0003_auto_20160515_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodtopic',
            name='total_collects',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='收藏数'),
        ),
    ]
