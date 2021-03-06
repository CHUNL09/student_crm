# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 17:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_auto_20160616_0116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classlist',
            options={},
        ),
        migrations.AlterModelOptions(
            name='consultrecord',
            options={},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={},
        ),
        migrations.AlterModelOptions(
            name='courserecord',
            options={},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={},
        ),
        migrations.AlterModelOptions(
            name='studyrecord',
            options={'permissions': (('view_statics', '查看班级统计信息'), ('search_statics', '搜索班级统计信息'))},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('view_records', '查看记录'), ('view_index', '查看主页'), ('del_records', '删除记录'))},
        ),
    ]
