from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from app01 import models
from app01 import myforms
import json
import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from app01.permissions import check_permission
# Create your views here.

@check_permission
@login_required
def statics(request):
    course_obj=models.CourseRecord.objects.all()
    if request.method=='POST':
        #request.POST['iclass']
        query_res=models.StudyRecord.objects.filter(course_record=int(request.POST['iclass'])).all()
        return render(request,'statics.html',{'course_list':course_obj,'items':query_res,'display':True,'group':request.user.groups.all()[0].name})
    else:
        return render(request,'statics.html',{'course_list':course_obj,'display':False,'group':request.user.groups.all()[0].name})



@login_required
def add(request):
    if request.method=='POST':
        print("this is post")
        if request.POST['add_action']=='add_userprofile':
            print(request.POST)
            user_obj=User.objects.get(pk=int(request.POST['user']))
            print(user_obj,type(user_obj))
            form_data={
                'user':request.POST['user'],
                'name':request.POST['name']
            }
            request_form=myforms.UserProfileForm(form_data)
            if request_form.is_valid():
                add_data={
                     'user':user_obj,
                    'name':request.POST['name']
                }
                new_profile=models.UserProfile(**add_data)
                new_profile.save()
                return HttpResponseRedirect('/index')
            else:
                print(request_form.errors)
                return render(request,'error.html',{'errors':request_form.errors,'group':request.user.groups.all()[0].name})
        elif request.POST['add_action']=='add_course':
            print(request.POST)
            form_data={
                'name':request.POST['name'],
                'price':request.POST['price'],
                'online_price':request.POST['online_price'],
                'brief':request.POST['brief'],
            }
            request_form=myforms.CourseForm(form_data)
            if request_form.is_valid():
                new_profile=models.Course(**form_data)
                new_profile.save()
                return HttpResponseRedirect('/index')
            else:
                print(request_form.errors)
                return render(request,'error.html',{'errors':request_form.errors,'group':request.user.groups.all()[0].name})
        elif request.POST['add_action']=='add_classlist':
            # teach=request.POST.getlist('teachers')
            # print(teach,type(teach))
            form_data={
                'course':request.POST['course'],
                'course_type':request.POST['course_type'],
                'semester':request.POST['semester'],
                'start_date_month': request.POST['start_date_month'],
                'start_date_day': request.POST['start_date_day'],
                'start_date_year': request.POST['start_date_year'],
                'graduate_date_year': request.POST['graduate_date_year'],
                'graduate_date_month': request.POST['graduate_date_month'],
                'graduate_date_day': request.POST['graduate_date_day'],
                'teachers': request.POST.getlist('teachers'),
            }
            request_form=myforms.ClassListForm(form_data)
            if request_form.is_valid():
                course_obj=models.Course.objects.get(pk=int(request.POST['course']))
                teachers_obj=[]
                for item in request.POST.getlist('teachers'):
                    teacher_obj=models.UserProfile.objects.get(pk=int(item))
                    teachers_obj.append(teacher_obj)
                if int(request.POST['graduate_date_year'])==0 or int(request.POST['graduate_date_month'])==0 or int(request.POST['graduate_date_day'])==0:
                    graduate_date_value=None
                else:
                    graduate_date_value="%s-%s-%s"%(int(request.POST['graduate_date_year']),
                                                 int(request.POST['graduate_date_month']),
                                              int(request.POST['graduate_date_day']))

                add_data={
                    'course':course_obj,
                    'course_type':request.POST['course_type'],
                    'semester':int(request.POST['semester']),
                    'start_date': "%s-%s-%s"%(int(request.POST['start_date_year']),int(request.POST['start_date_month']),
                                              int(request.POST['start_date_day'])),
                    'graduate_date': graduate_date_value,
                }
                new_classlist=models.ClassList(**add_data)
                new_classlist.save()
                classlist_obj=models.ClassList.objects.filter(course=add_data['course'],
                                                              course_type=add_data['course_type'],
                                                              semester=add_data['semester']).first()
                for teacher_obj in teachers_obj:
                    classlist_obj.teachers.add(teacher_obj)
                classlist_obj.save()
                return HttpResponseRedirect('/index')
            else:
                print(request_form.errors)
                return render(request,'error.html',{'errors':request_form.errors,'group':request.user.groups.all()[0].name})
        elif request.POST['add_action']=='add_customer':
            print("customer_data",request.POST)
            form_data={
                'qq':request.POST['qq'],
                'name':request.POST['name'],
                'phone':int(request.POST['phone']),
                'stu_id':request.POST['stu_id'],
                'source':request.POST['source'],
                'referral_from':request.POST['referral_from'],  # 可能需要修改
                'course':request.POST['course'],
                'class_type':request.POST['class_type'],
                'customer_note':request.POST['customer_note'],
                'status':request.POST['status'],
                'consultant':request.POST['consultant'],
                #'date':request.POST['date'],   auto_add 属性后前台页面不显示这个字段
                'class_list':request.POST.getlist('class_list'),
            }
            request_form=myforms.CustomerForm(form_data)
            if request_form.is_valid():

                if request.POST['referral_from']=='':
                    referral_num=0
                else:
                    referral_num=int(request.POST['referral_from'])
                referral_obj=models.Customer.objects.filter(pk=referral_num).first()
                course_obj=models.Course.objects.get(pk=int(request.POST['course']))
                consultant_obj=models.UserProfile.objects.get(pk=int(request.POST['consultant']))
                class_list_obj=[]
                for item in request.POST.getlist('class_list'):
                    clist_obj=models.ClassList.objects.get(pk=int(item))
                    class_list_obj.append(clist_obj)

                add_data={
                    'qq':request.POST['qq'],
                    'name':request.POST['name'],
                    'phone':int(request.POST['phone']),
                    'stu_id':request.POST['stu_id'],
                    'source':request.POST['source'],
                    'referral_from':referral_obj,  # 可能需要修改
                    'course':course_obj,
                    'class_type':request.POST['class_type'],
                    'customer_note':request.POST['customer_note'],
                    'status':request.POST['status'],
                    'consultant':consultant_obj,
                }
                new_customer=models.Customer(**add_data)
                new_customer.save()
                customer_obj=models.Customer.objects.filter(qq=add_data['qq']).first()
                for clist_obj in class_list_obj:
                    customer_obj.class_list.add(clist_obj)
                customer_obj.save()
                return HttpResponseRedirect('/index')
            else:
                print(request_form.errors)
                return render(request,'error.html',{'errors':request_form.errors,'group':request.user.groups.all()[0].name})
        elif request.POST['add_action']=='add_consultrecord':
            print("consultant_data",request.POST)
            form_data={
                'customer':request.POST['customer'],
                'note':request.POST['note'],
                'status':request.POST['status'],
                'consultant':request.POST['consultant'],
                #'date':request.POST['date'],   auto_add 属性后前台页面不显示这个字段
            }
            request_form=myforms.ConsultRecordForm(form_data)
            if request_form.is_valid():

                customer_obj=models.Customer.objects.filter(pk=int(request.POST['customer'])).first()
                consultant_obj=models.UserProfile.objects.get(pk=int(request.POST['consultant']))

                add_data={
                    'customer':customer_obj,
                    'note':request.POST['note'],
                    'status':request.POST['status'],
                    'consultant':consultant_obj,
                }
                new_consultrecord=models.ConsultRecord(**add_data)
                new_consultrecord.save()
                return HttpResponseRedirect('/index')
            else:
                print(request_form.errors)
                return render(request,'error.html',{'errors':request_form.errors,'group':request.user.groups.all()[0].name})
        elif request.POST['add_action']=='add_courserecord':
            print("courserecord_data",request.POST)
            form_data={
                'course':request.POST['course'],
                'day_num':int(request.POST['day_num']),
                'teacher':request.POST['teacher']
            }
            request_form=myforms.CourseRecordForm(form_data)
            if request_form.is_valid():

                course_obj=models.ClassList.objects.filter(pk=int(request.POST['course'])).first()
                teacher_obj=models.UserProfile.objects.get(pk=int(request.POST['teacher']))

                add_data={
                    'course':course_obj,
                    'day_num':int(request.POST['day_num']),
                    'teacher':teacher_obj
                }
                new_courserecord=models.CourseRecord(**add_data)
                new_courserecord.save()
                return HttpResponseRedirect('/index')
            else:
                print(request_form.errors)
                return render(request,'error.html',{'errors':request_form.errors,'group':request.user.groups.all()[0].name})
        elif request.POST['add_action']=='add_studyrecord':
            print("studyrecord_data",request.POST)
            form_data={

                'course_record':request.POST['course_record'],
                'student':request.POST['student'],
                'record':request.POST['record'],
                'score':int(request.POST['score']),
                'note':request.POST['note'],
            }
            request_form=myforms.StudyRecordForm(form_data)
            if request_form.is_valid():

                course_record_obj=models.CourseRecord.objects.filter(pk=int(request.POST['course_record'])).first()
                student_obj=models.Customer.objects.get(pk=int(request.POST['student']))

                add_data={

                    'course_record':course_record_obj,
                    'student':student_obj,
                    'record':request.POST['record'],
                    'score':int(request.POST['score']),
                    'note':request.POST['note'],
                }
                new_studyrecord=models.StudyRecord(**add_data)
                new_studyrecord.save()
                return HttpResponseRedirect('/index')
            else:
                print(request_form.errors)
                return render(request,'error.html',{'errors':request_form.errors,'group':request.user.groups.all()[0].name})
    else:
        print("this is get")
        if request.GET['action']=='add_userprofile':
            profiles=myforms.UserProfileForm()
            return render(request,"add.html",{'addprofiles':profiles,'t_user_profile':'true','group':request.user.groups.all()[0].name})
        elif request.GET['action']=='add_course':
            course=myforms.CourseForm()
            return render(request,"add.html",{'addcourses':course,'t_course':'true','group':request.user.groups.all()[0].name})
        elif request.GET['action']=='add_classlist':
            classlists=myforms.ClassListForm()
            return render(request,"add.html",{'addclasslist':classlists,'t_classlist':'true','group':request.user.groups.all()[0].name})
        elif request.GET['action']=='add_customer':
            customers=myforms.CustomerForm()
            return render(request,"add.html",{'addcustomer':customers,'t_customer':'true','group':request.user.groups.all()[0].name})
        elif request.GET['action']=='add_consultrecord':
            consultrecords=myforms.ConsultRecordForm()
            return render(request,"add.html",{'addconsultrecord':consultrecords,'t_consultrecord':'true','group':request.user.groups.all()[0].name})
        elif request.GET['action']=='add_courserecord':
            courserecords=myforms.CourseRecordForm()
            return render(request,"add.html",{'addcourserecord':courserecords,'t_courserecord':'true','group':request.user.groups.all()[0].name})
        elif request.GET['action']=='add_studyrecord':
            studyrecords=myforms.StudyRecordForm()
            return render(request,"add.html",{'addstudyrecord':studyrecords,'t_studyrecord':'true','group':request.user.groups.all()[0].name})


@login_required
@check_permission
def delete(request):
    if request.method=="POST":
        print(request.POST)
        if request.POST['table_val']=='t_user_profile':
            models.UserProfile.objects.filter(id=int(request.POST['pk_val'])).delete()
            data={
                'res':'success',
                'msg':'Delete User Profile Record Successfully!'
            }
            return HttpResponse(json.dumps(data))
        elif request.POST['table_val']=='t_course':
            models.Course.objects.filter(id=int(request.POST['pk_val'])).delete()
            data={
                'res':'success',
                'msg':'Delete Course Record Successfully!'
            }
            return HttpResponse(json.dumps(data))
        elif request.POST['table_val']=='t_classlist':
            models.ClassList.objects.filter(id=int(request.POST['pk_val'])).delete()
            data={
                'res':'success',
                'msg':'Delete ClassList Record Successfully!'
            }
            return HttpResponse(json.dumps(data))
        elif request.POST['table_val']=='t_customer':
            models.Customer.objects.filter(id=int(request.POST['pk_val'])).delete()
            data={
                'res':'success',
                'msg':'Delete Customer Record Successfully!'
            }
            return HttpResponse(json.dumps(data))
        elif request.POST['table_val']=='t_consultrecord':
            models.ConsultRecord.objects.filter(id=int(request.POST['pk_val'])).delete()
            data={
                'res':'success',
                'msg':'Delete ConsultRecord Successfully!'
            }
            return HttpResponse(json.dumps(data))
        elif request.POST['table_val']=='t_courserecord':
            models.CourseRecord.objects.filter(id=int(request.POST['pk_val'])).delete()
            data={
                'res':'success',
                'msg':'Delete CourseRecord Successfully!'
            }
            return HttpResponse(json.dumps(data))
        elif request.POST['table_val']=='t_studyrecord':
            models.StudyRecord.objects.filter(id=int(request.POST['pk_val'])).delete()
            data={
                'res':'success',
                'msg':'Delete StudyRecord Successfully!'
            }
            return HttpResponse(json.dumps(data))
        else:
            data={
                'res':'failed',
                'msg':'Delete Record Failed!'
            }
            return HttpResponse(json.dumps(data))
    if request.method=="GET":
        print(request.GET)
        return HttpResponse("OK")

@login_required
def edit(request):
    if request.method=='GET':
        if request.GET['tablename']=='t_user_profile':
            user_obj=models.UserProfile.objects.filter(id=int(request.GET['pkvalue'])).first()
            form_data={
                'user':user_obj.user_id,
                'name':user_obj.name,
            }
            users=myforms.UserProfileForm(form_data)
            return render(request,'edit.html',{'editprofiles':users,'t_user_profile':'true',
                                                'id_value':int(request.GET['pkvalue']),
                                               'group':request.user.groups.all()[0].name})

        elif request.GET['tablename']=='t_course':
            course_obj=models.Course.objects.filter(id=int(request.GET['pkvalue'])).first()
            form_data={
                'name':course_obj.name,
                'price':course_obj.price,
                'online_price':course_obj.online_price,
                'brief':course_obj.brief,
            }
            courses=myforms.CourseForm(form_data)
            return render(request,'edit.html',{'editcourses':courses,'t_course':'true',
                                               'id_value':int(request.GET['pkvalue']),
                                               'group':request.user.groups.all()[0].name})

        elif request.GET['tablename']=='t_classlist':
            classlist_obj=models.ClassList.objects.filter(id=int(request.GET['pkvalue'])).first()
            t_list=[]
            for item in classlist_obj.teachers.values():
                t_list.append(int(item['id']))
            form_data={
                'course':classlist_obj.course_id,
                'course_type':classlist_obj.course_type,
                'semester':classlist_obj.semester,
                'start_date':classlist_obj.start_date,
                'graduate_date':classlist_obj.graduate_date,
                'teachers':t_list,
            }
            classlists=myforms.ClassListForm(form_data)
            return render(request,'edit.html',{'editclasslist':classlists,'t_classlist':'true',
                                               'id_value':int(request.GET['pkvalue']),
                                               'group':request.user.groups.all()[0].name})

        elif request.GET['tablename']=='t_customer':
            customer_obj=models.Customer.objects.filter(id=int(request.GET['pkvalue'])).first()
            c_list=[]
            for item in customer_obj.class_list.values():
                c_list.append(int(item['id']))
            form_data={
                'qq':customer_obj.qq,
                'name':customer_obj.name,
                'phone':customer_obj.phone,
                'stu_id':customer_obj.stu_id,
                'source':customer_obj.source,
                'referral_from':customer_obj.referral_from_id,
                'course':customer_obj.course_id,
                'class_type':customer_obj.class_type,
                'customer_note':customer_obj.customer_note,
                'status':customer_obj.status,
                'consultant':customer_obj.consultant_id,
                'date':customer_obj.date,
                'class_list':c_list,
            }
            customers=myforms.CustomerForm(form_data)
            return render(request,'edit.html',{'editcustomer':customers,'t_customer':'true',
                                               'id_value':int(request.GET['pkvalue']),
                                               'group':request.user.groups.all()[0].name})

        elif request.GET['tablename']=='t_consultrecord':
            consultrecord_obj=models.ConsultRecord.objects.filter(id=int(request.GET['pkvalue'])).first()
            form_data={
                'customer':consultrecord_obj.customer_id,
                'note':consultrecord_obj.note,
                'status':consultrecord_obj.status,
                'consultant':consultrecord_obj.consultant_id,
                'date':consultrecord_obj.date,
            }
            consultrecords=myforms.ConsultRecordForm(form_data)
            return render(request,'edit.html',{'editconsultrecord':consultrecords,'t_consultrecord':'true',
                                               'id_value':int(request.GET['pkvalue']),
                                               'group':request.user.groups.all()[0].name})

        elif request.GET['tablename']=='t_courserecord':
            courserecord_obj=models.CourseRecord.objects.filter(id=int(request.GET['pkvalue'])).first()
            form_data={
                'course':courserecord_obj.course_id,
                'day_num':courserecord_obj.day_num,
                'date':courserecord_obj.date,
                'teacher':courserecord_obj.teacher_id,
            }
            courserecords=myforms.CourseRecordForm(form_data)
            return render(request,'edit.html',{'editcourserecord':courserecords,'t_courserecord':'true',
                                               'id_value':int(request.GET['pkvalue']),
                                               'group':request.user.groups.all()[0].name})

        elif request.GET['tablename']=='t_studyrecord':
            studyrecord_obj=models.StudyRecord.objects.filter(id=int(request.GET['pkvalue'])).first()
            form_data={
                'course_record':studyrecord_obj.course_record_id,
                'student':studyrecord_obj.student_id,
                'record':studyrecord_obj.record,
                'score':studyrecord_obj.score,
                'date':studyrecord_obj.date,
                'note':studyrecord_obj.note,
            }
            studyrecords=myforms.StudyRecordForm(form_data)
            return render(request,'edit.html',{'editstudyrecord':studyrecords,'t_studyrecord':'true',
                                               'id_value':int(request.GET['pkvalue']),
                                               'group':request.user.groups.all()[0].name})
        else:
            return render(request,'error.html',{'errors':'404 link','group':request.user.groups.all()[0].name})
    else:
        print("this is post")
        if request.POST['edit_action']=='edit_userprofile':
            print(request.POST)
            models.UserProfile.objects.filter(id=int(request.POST['pk_val'])).update(user=request.POST['user'],
                                                                                      name=request.POST['name'])
            # userprofile_obj.save()
            return HttpResponseRedirect('/index')

        elif request.POST['edit_action']=='edit_course':
            print(request.POST)
            models.Course.objects.filter(id=int(request.POST['pk_val'])).update(name=request.POST['name'],
                                                                                 price=int(request.POST['price']),
                                                                    online_price=int(request.POST['online_price']),
                                                                                brief=request.POST['brief'],)
            return HttpResponseRedirect('/index')
        elif request.POST['edit_action']=='edit_classlist':
            print(request.POST)
            teacher_list=[]
            for item in request.POST.getlist('teachers'):
                teacher_list.append(int(item))
            if int(request.POST['graduate_date_year'])==0 or int(request.POST['graduate_date_month'])==0 or int(request.POST['graduate_date_day'])==0:
                graduate_date_value=None
            else:
                graduate_date_value="%s-%s-%s"%(int(request.POST['graduate_date_year']),
                                             int(request.POST['graduate_date_month']),
                                          int(request.POST['graduate_date_day']))
            old_teachers=models.ClassList.objects.filter(id=int(request.POST['pk_val'])).values('teachers')
            new_obj=models.ClassList.objects.filter(id=int(request.POST['pk_val'])).first()
            #to_be_deleted=[]
            for i in list(old_teachers):
                # print(i,type(i),"--------------------")
                tmp=models.UserProfile.objects.filter(id=i['teachers']).first()
                #to_be_deleted.append(tmp)
                # print("--before remove",new_obj.teachers)
                # print(tmp)
                new_obj.teachers.remove(tmp)
                # print("--after remove",new_obj.teachers)
            #to_be_added=[]
            for i in request.POST.getlist('teachers'):
                teacher_obj=models.UserProfile.objects.get(id=int(i))
                # print("--before add",new_obj.teachers)
                # print(teacher_obj)
                new_obj.teachers.add(teacher_obj)
                new_obj.save()
                # print("--after add",new_obj.teachers)
                models.ClassList.objects.filter(id=int(request.POST['pk_val'])).update(course=int(request.POST['course']),
                course_type=request.POST['course_type'],
                semester=int(request.POST['semester']),
                start_date="%s-%s-%s"%(int(request.POST['start_date_year']),
                                                 int(request.POST['start_date_month']),
                                              int(request.POST['start_date_day'])),
                graduate_date=graduate_date_value,
                )
            return HttpResponseRedirect('/index')

        elif request.POST['edit_action']=='edit_customer':
            print(request.POST)
            old_classlist=models.Customer.objects.filter(id=int(request.POST['pk_val'])).values('class_list')
            new_obj=models.Customer.objects.filter(id=int(request.POST['pk_val'])).first()
            for i in list(old_classlist):
                tmp=models.ClassList.objects.filter(id=i['class_list']).first()
                new_obj.class_list.remove(tmp)
            for i in request.POST.getlist('class_list'):
                clist_obj=models.ClassList.objects.get(id=int(i))
                new_obj.class_list.add(clist_obj)
                new_obj.save()

            models.Customer.objects.filter(id=int(request.POST['pk_val'])).update(qq=request.POST['qq'],
            name=request.POST['name'],
            phone = int(request.POST['phone']),
            stu_id= request.POST['stu_id'],
            source =request.POST['source'] ,
            referral_from=int(request.POST['referral_from']),
            course=int(request.POST['course']),
            class_type=request.POST['class_type'],
            customer_note=request.POST['customer_note'],
            status=request.POST['status'],
            consultant=int(request.POST['consultant']),
           )
            return HttpResponseRedirect('/index')
        elif request.POST['edit_action']=='edit_consultrecord':
            print(request.POST)
            models.ConsultRecord.objects.filter(id=int(request.POST['pk_val'])).update(customer=int(request.POST['customer']),
                                                                                 note=request.POST['note'],
                                                                    status=int(request.POST['status']),
                                                                                consultant=int(request.POST['consultant']),)
            return HttpResponseRedirect('/index')
        elif request.POST['edit_action']=='edit_courserecord':
            print(request.POST)
            models.CourseRecord.objects.filter(id=int(request.POST['pk_val'])).update(course=int(request.POST['course']),
                                                                                 day_num=int(request.POST['day_num']),
                                                                                teacher=int(request.POST['teacher']),)
            return HttpResponseRedirect('/index')
        elif request.POST['edit_action']=='edit_studyrecord':
            print(request.POST)
            models.StudyRecord.objects.filter(id=int(request.POST['pk_val'])).update(course_record=int(request.POST['course_record']),
                                                                                 student=int(request.POST['student']),
                                                                                record=request.POST['record'],
                                                                                   score=int(request.POST['score']),
                                                                                note=request.POST['note'],)
            return HttpResponseRedirect('/index')

@login_required
def dashboard(request):
    # test_res=models.UserProfile.objects.filter(id=5).first()
    # print(test_res.user.get_group_permissions(),"print group here----")
    # print(request.user.groups.all()[0].name,"hello---------")
    cur_group=request.user.groups.all()[0].name
    return render(request,'index.html',{'group':cur_group,'group':request.user.groups.all()[0].name})

def mylogin(request):
    if request.method=='POST':
        login_user=authenticate(username=request.POST['username'],
                                password=request.POST['password'])
        if login_user is not None:
            login(request,login_user)
            return HttpResponseRedirect('/index')
        else:
            print("username and password were incorrect.")
            return HttpResponse("login failed!")
    else:
        user_list=models.UserProfile.objects.all()
        return render(request,"login.html")

def mylogout(request):
    logout(request)
    return HttpResponse("logout ok")

@login_required
@check_permission
def admin(request):
    # test_res=models.UserProfile.objects.filter(id=5).first()
    # print(test_res.user.get_group_permissions(),"print group here----")
    # print(request.user.groups.all()[0].name,"hello---------")
    if request.method=='POST':

        if request.POST['action']=='view_userprofile':
            user_list=models.UserProfile.objects.all()
            paginator=Paginator(user_list,2)
            page=request.POST.get('page')
            try:
                user_obj=paginator.page(page)
            except PageNotAnInteger:
                user_obj=paginator.page(1)
            except EmptyPage:
                user_obj=paginator.page(paginator.num_pages)
            return render(request,'show_data.html',{'items':user_obj,'t_user_profile':'true','group':request.user.groups.all()[0].name})
        elif request.POST['action']=='view_course':
            course_list=models.Course.objects.all()
            return render(request,'show_data.html',{'items':course_list,'t_course':'true','group':request.user.groups.all()[0].name})
        elif request.POST['action']=='view_classlist':
            classlists=models.ClassList.objects.all()
            return render(request,'show_data.html',{'items':classlists,'t_classlist':'true','group':request.user.groups.all()[0].name})
        elif request.POST['action']=='view_customer':
            customers=models.Customer.objects.all()
            return render(request,'show_data.html',{'items':customers,'t_customer':'true','group':request.user.groups.all()[0].name})
        elif request.POST['action']=='view_consultrecord':
            consultrecords=models.ConsultRecord.objects.all()
            return render(request,'show_data.html',{'items':consultrecords,'t_consultrecord':'true','group':request.user.groups.all()[0].name})
        elif request.POST['action']=='view_courserecord':
            courserecords=models.CourseRecord.objects.all()
            return render(request,'show_data.html',{'items':courserecords,'t_courserecord':'true','group':request.user.groups.all()[0].name})
        elif request.POST['action']=='view_studyrecord':
            studyrecords=models.StudyRecord.objects.all()
            return render(request,'show_data.html',{'items':studyrecords,'t_studyrecord':'true','group':request.user.groups.all()[0].name})
        else:
            return render(request,'error.html',{'errors':'404 link','group':request.user.groups.all()[0].name})

    else:
        print("this is get here")
        #user_list=models.UserProfile.objects.all()
        # for user in user_list:
        #     print("---",user.user_id,user.name)
        return HttpResponseRedirect('/crm/dashboard')