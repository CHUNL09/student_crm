# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 16:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20160615_2356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classlist',
            options={'permissions': (('view_classlist', '查看classlist记录'),)},
        ),
        migrations.AlterModelOptions(
            name='consultrecord',
            options={'permissions': (('view_consultrecord', '查看咨询记录'),)},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'permissions': (('view_course', '查看course记录'),)},
        ),
        migrations.AlterModelOptions(
            name='courserecord',
            options={'permissions': (('view_courserecord', '查看课程记录'),)},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': (('view_customer', '查看customer记录'),)},
        ),
        migrations.AlterModelOptions(
            name='studyrecord',
            options={'permissions': (('view_studyrecord', '查看学习记录'), ('view_statics', '查看班级统计信息'))},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('view_userprofile', '查看userprofile记录'),)},
        ),
    ]
