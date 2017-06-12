from django import forms
from django.forms import ModelForm
from app01 import models

class UserProfileForm(ModelForm):
    class Meta:
        model=models.UserProfile
        fields='__all__'
        widgets={
            'user':forms.Select(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
        }

class CourseForm(ModelForm):
    class Meta:
        model=models.Course
        fields='__all__'
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={'class':'form-control'}),
            'online_price':forms.TextInput(attrs={'class':'form-control'}),
            'brief':forms.Textarea(attrs={'class':'form-control'}),
        }

class ClassListForm(ModelForm):
    class Meta:
        model=models.ClassList
        fields='__all__'
        widgets={
            'course':forms.Select(attrs={'class':'form-control'}),
            'course_type':forms.Select(attrs={'class':'form-control'}),
            'semester':forms.TextInput(attrs={'class':'form-control'}),
            'start_date':forms.SelectDateWidget(
                                                empty_label=("Year", "Month", "Day"),),
            'graduate_date':forms.SelectDateWidget(
                                                   empty_label=("Year", "Month", "Day"),),
            'teachers':forms.SelectMultiple(attrs={'class':'form-control'}),
        }

class CustomerForm(ModelForm):
    class Meta:
        model=models.Customer
        fields='__all__'
        widgets={
            'qq':forms.TextInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'stu_id':forms.TextInput(attrs={'class':'form-control'}),
            'source':forms.Select(attrs={'class':'form-control'}),
            'referral_from':forms.Select(attrs={'class':'form-control'}),
            'course':forms.Select(attrs={'class':'form-control'}),
            'class_type':forms.Select(attrs={'class':'form-control'}),
            'customer_note':forms.Textarea(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'consultant':forms.Select(attrs={'class':'form-control'}),
            'date':forms.SelectDateWidget(empty_label=("Year", "Month", "Day")),
            # 'graduate_date':forms.SelectDateWidget(
            #                                        empty_label=("Year", "Month", "Day"),),
            'class_list':forms.SelectMultiple(attrs={'class':'form-control'}),
        }

class ConsultRecordForm(ModelForm):
    class Meta:
        model=models.ConsultRecord
        fields='__all__'
        widgets={
            'customer':forms.Select(attrs={'class':'form-control'}),
            'note':forms.Textarea(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'consultant':forms.Select(attrs={'class':'form-control'}),
            'date':forms.SelectDateWidget(empty_label=("Year", "Month", "Day")),
        }

class CourseRecordForm(ModelForm):
    class Meta:
        model=models.CourseRecord
        fields='__all__'
        widgets={
            'course':forms.Select(attrs={'class':'form-control'}),
            'day_num':forms.TextInput(attrs={'class':'form-control'}),
            'date':forms.SelectDateWidget(empty_label=("Year", "Month", "Day")),
            'teacher':forms.Select(attrs={'class':'form-control'}),
        }

class StudyRecordForm(ModelForm):
    class Meta:
        model=models.StudyRecord
        fields='__all__'
        widgets={
            'course_record':forms.Select(attrs={'class':'form-control'}),
            'student':forms.Select(attrs={'class':'form-control'}),
            'record':forms.Select(attrs={'class':'form-control'}),
            'score':forms.Select(attrs={'class':'form-control'}),
            'date':forms.SelectDateWidget(empty_label=("Year", "Month", "Day")),
            'note':forms.Textarea(attrs={'class':'form-control'}),
        }