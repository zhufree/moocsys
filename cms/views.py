#-*- coding:utf-8 -*-
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.context_processors import csrf
from django.template.loader import get_template
from django.contrib.auth.models import User
import re
from django.shortcuts import render_to_response,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext 
from cms.models import *
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from getcourses import *
# Create your views here.
@csrf_exempt
def home_page(request):
    #'''
    coursesInfo=getcourseinfo()
    #print coursesInfo
    coursesNum=len(coursesInfo[0])
    for i in range(coursesNum):
        if User.objects.filter(username=coursesInfo[1][i]):
            cur_user=User.objects.filter(username=coursesInfo[1][i])[0]
        else:
            cur_user=User.objects.create_user(
                username=coursesInfo[1][i], 
                email="example@example.com", 
                password="")
            cur_user.save()
        if Teacher.objects.filter(user=cur_user):
            cur_teacher=Teacher.objects.filter(user=cur_user)[0]
        else:
            cur_teacher=Teacher.objects.create(
                user=cur_user,
                school=coursesInfo[2][i]
                )
            cur_teacher.save()
        if Course.objects.filter(name=coursesInfo[0][i]):
            cur_course=Course.objects.filter(name=coursesInfo[0][i])
        else:
            cur_course=Course.objects.create(
                name=coursesInfo[0][i],
                teacher=cur_teacher,
                img_url=coursesInfo[3][i]
                )
            cur_course.save()
    #'''
    courses=Course.objects.all()#获取并在首页显示所有课程
    variables=RequestContext(request,{'courses':courses})
    return render_to_response('index.html',variables)

@csrf_exempt
#加入课程
def join_page(request):
    if request.method=='POST':
        cur_user=request.user#获取当前用户
        cur_course=Course.objects.get(pk=int(request.POST.get('courseid')))#获取当前页面的课程
        cur_course.course_student.add(cur_user.user_student)#在课程的参与学生中加入用户
        cur_course.attendance+=1#参与人数加1
        cur_course.save()
        cur_user.user_student.courses.add(cur_course)#在用户的参与课程中加入当前课程
        cur_user.save()
        return HttpResponseRedirect('/course/%d'%cur_course.id)#返回课程页面
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
#发布（讨论，帖子等）
def post_page(request):
    if request.method=='POST':
        cur_user=request.user#获取当前用户
        post_type=request.POST.get('post_type')
        if post_type=='course_discuss':
            cur_course=Course.objects.get(pk=int(request.POST.get('courseid')))#获取当前页面的课程
            cur_discuss=Discuss.objects.create(
                name=request.POST.get('title'),
                content=request.POST.get('content'),
                course=cur_course,
                )
            if cur_user.has_perm('user_student'):
                cur_discuss.student=cur_user.user_student
            elif cur_user.has_perm('user_teacher'):
                cur_discuss.teacher=cur_user.user_teacher
            cur_discuss.save()
            return HttpResponseRedirect('/course/%d'%cur_course.id)#返回课程页面
        elif post_type=='question':
            cur_course=Course.objects.get(pk=int(request.POST.get('courseid')))#获取当前页面的课程
            cur_question=Question.objects.create(
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                quizzer=cur_user.user_student,
                course=cur_course,
                )
            cur_question.save()
            return HttpResponseRedirect('/course/%d'%cur_course.id)#返回课程页面
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def login_page(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('disabled account')
        else:
            return HttpResponse('invalid login')
    return render_to_response('registration/login.html',RequestContext(request))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
@csrf_exempt
def profile_page(request):
    cur_user=request.user
    if request.method=='POST':
        if cur_user.has_perm('user_student'):
            newStuid=request.POST.get('changeStuid')
            newSchool=request.POST.get('changeSchool')
            newMajor=request.POST.get('changeMajor')
            newPassword=request.POST.get('changePassword')
            cur_user.user_student.studentid=newStuid
            cur_user.user_student.school=newSchool
            cur_user.user_student.major=newMajor
            cur_user.set_password(newPassword)
            cur_user.user_student.save()
            cur_user.save()
        elif cur_user.has_perm('user_teacher'):
            newSchool=request.POST.get('changeSchool')
            newPassword=request.POST.get('changePassword')
            cur_user.user_teacher.school=newSchool
            cur_user.set_password(newPassword)
            cur_user.user_teacher.save()
            cur_user.save()
    if cur_user.has_perm('user_student'):
        courses=cur_user.user_student.courses.all()
    elif cur_user.has_perm('user_teacher'):
        courses=cur_user.user_teacher.courses.all()
    else:
        courses={}
    return render_to_response('profile.html',RequestContext(request,{'courses':courses}))

@csrf_exempt
def course_page(request,id):
    cur_course=Course.objects.get(pk=id)
    cur_user=request.user
    if cur_user.has_perm('user_student'):
        is_student=True
        if cur_course in cur_user.user_student.courses.all():
            is_attended=True
        else:
            is_attended=False
    else:
        is_student=False
        if cur_course.teacher==cur_user:
            is_attended=True
        else:
            is_attended=False
   # print is_student,is_attended
    if cur_course.course_discuss.all():
        discusses=cur_course.course_discuss.all()
    else:
        discusses={}
    if cur_course.course_question.all():
        questions=cur_course.course_question.all()
    else:
        questions={}
    return render_to_response('course.html',RequestContext(request,{
        'course':cur_course,
        'discusses':discusses,
        'questions':questions,
        'is_student':is_student,
        'is_attended':is_attended,
        }))