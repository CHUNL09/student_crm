from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class_type_choice=(
    ('online',u'网络班'),
    ('offline_weekend',u'面授班(周末)'),
    ('offline_fulltime',u'面授班(脱产)'),
)


class UserProfile(models.Model):
    user=models.OneToOneField(User)
    name=models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("view_records", "查看记录"),
            ("view_index", "查看主页"),
            ("del_records", "删除记录"),
        )

class School(models.Model):
    name=models.CharField(max_length=64,unique=True)
    addr=models.CharField(max_length=128)
    staff=models.ManyToManyField('UserProfile',blank=True)
    def __str__(self):
        return self.name

class Course(models.Model):
    name=models.CharField(max_length=128,unique=True)
    price=models.IntegerField(default=0)
    online_price=models.IntegerField(default=0)
    brief=models.TextField()
    def __str__(self):
        return self.name



class ClassList(models.Model):
    course=models.ForeignKey('Course')
    course_type=models.CharField(choices=class_type_choice,max_length=32)
    semester=models.IntegerField()
    start_date=models.DateField()
    graduate_date=models.DateField(blank=True,null=True)
    teachers=models.ManyToManyField('UserProfile',blank=True)
    def __str__(self):
       return "%s(%s)" %(self.course.name,self.course_type)



class Customer(models.Model):
    qq=models.CharField(max_length=64,unique=True)
    name=models.CharField(max_length=32,blank=True)
    phone=models.BigIntegerField(blank=True,null=True)
    stu_id=models.CharField(blank=True,null=True,max_length=128)
    source_type=(('qq',u'qq群'),
                 ('referral',u'内部转介绍'),
                 ('51cto',u'51cto'),
                 ('agent',u'招生代理'),
                 ('others',u'其他'),
                 )
    source=models.CharField(choices=source_type,default='qq',max_length=32)
    referral_from=models.ForeignKey('self',blank=True,null=True,related_name='internal_referral')
    course=models.ForeignKey('Course')
    class_type=models.CharField(choices=class_type_choice,max_length=64)
    customer_note=models.TextField()
    status_choices=(
                ('signed',u'已报名'),
                 ('unregistered',u'未报名'),
                 ('graduated',u'已毕业'),
    )
    status=models.CharField(choices=status_choices,max_length=64)
    consultant=models.ForeignKey('UserProfile')
    date=models.DateField(auto_now_add=True)
    class_list=models.ManyToManyField('ClassList',blank=True)

    def __str__(self):
        return "%s(%s)" %(self.qq,self.name)



class ConsultRecord(models.Model):
    customer=models.ForeignKey('Customer')
    note=models.TextField()
    status_choices=(
                (1,u'近期无报名计划'),
                 (2,u'2个月内报名'),
                 (3,u'1个月内报名'),
                (4,u'2周内报名'),
                (5,u'1周内报名'),
                (6,u'2天内报名'),
                (7,u'已报名'),
    )
    status=models.IntegerField(choices=status_choices)
    consultant=models.ForeignKey('UserProfile')
    date=models.DateField(auto_now_add=True)



class CourseRecord(models.Model):
    course=models.ForeignKey('ClassList')
    day_num=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    teacher=models.ForeignKey('UserProfile')
    def __str__(self):
        return u"%s 第%s天" %(self.course,self.day_num)
    class Meta:
        unique_together=('course','day_num')


class StudyRecord(models.Model):
    course_record=models.ForeignKey('CourseRecord')
    student=models.ForeignKey('Customer')
    record_choices = (('checked', u"已签到"),
                      ('late',u"迟到"),
                      ('noshow',u"缺勤"),
                      ('leave_early',u"早退"),
                      )
    record=models.CharField(choices=record_choices,max_length=64)
    score_choices = ((100, 'A+'),
                     (90,'A'),
                     (85,'B+'),
                     (80,'B'),
                     (70,'B-'),
                     (60,'C+'),
                     (50,'C'),
                     (40,'C-'),
                     (0,'D'),
                     (-1,'N/A'),
                     (-100,'COPY'),
                     (-1000,'FAIL'),
                     )
    score=models.IntegerField(choices=score_choices,default=-1)
    date=models.DateField(auto_now_add=True)
    note=models.CharField(max_length=255,blank=True,null=True)
    class Meta:
        unique_together=('course_record','student')
        permissions = (
                ("view_statics", "查看班级统计信息"),
                ("search_statics", "搜索班级统计信息"),

            )