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
from cms.forms import *
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from getcourses import *
# Create your views here.
@csrf_exempt
def home_page(request):
    '''
    coursesInfo=getcourseinfo()
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
    '''
    courses=Course.objects.all()#获取并在首页显示所有课程
    variables=RequestContext(request,{'courses':courses})
    return render_to_response('index.html',variables)

def all_discuss_page(request):
    discusses=Discuss.objects.order_by('time')
    return render_to_response('all_discuss.html',RequestContext(request,{'discusses':discusses}))

def all_question_page(request):
    questions=Question.objects.order_by('time')
    return render_to_response('all_question.html',RequestContext(request,{'questions':questions}))

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
        if post_type=='course_discuss':#发布主题讨论
            cur_course=Course.objects.get(pk=int(request.POST.get('courseid')))#获取当前页面的课程
            cur_discuss=Discuss.objects.create(
                name=request.POST.get('title'),
                content=request.POST.get('content'),
                course=cur_course,
                )
            if hasattr(cur_user,'user_student'):
                cur_discuss.student=cur_user.user_student
            elif hasattr(cur_user,'user_teacher'):
                cur_discuss.teacher=cur_user.user_teacher
            cur_discuss.save()
            return HttpResponseRedirect('/course/%d'%cur_course.id)#返回课程页面
        elif post_type=='question':#发布问题
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
def register_page(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            cur_user=User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            cur_user.save()
            user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            login(request,user)
            user_type= request.POST.get('user_type')
            if user_type=='teacher':
                new_teacher=Teacher.objects.create(user=cur_user)
                new_teacher.save()
                cur_user.user_teacher=new_teacher
                cur_user.save()
            if user_type=='student':
                new_student=Student.objects.create(user=cur_user)
                new_student.save()
                cur_user.user_student=new_student
                cur_user.save()
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form=RegistrationForm()
    variables=RequestContext(request,{'form':form})
    return render_to_response('registration/register.html',RequestContext(request,{'form':form}))
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
@login_required
def profile_page(request):
    cur_user=request.user
    if request.method=='POST':
        if hasattr(cur_user,'user_student'):
            newStuid=request.POST.get('changeStuid')
            newSchool=request.POST.get('changeSchool')
            newMajor=request.POST.get('changeMajor')
            newPassword=request.POST.get('changePassword')#获取修改的属性值
            cur_user.user_student.studentid=newStuid
            cur_user.user_student.school=newSchool
            cur_user.user_student.major=newMajor#修改属性
            #cur_user.set_password(newPassword)这句没用= =
            cur_user.user_student.save()
            cur_user.save()
        elif hasattr(cur_user,'user_teacher'):
            newSchool=request.POST.get('changeSchool')
            newPassword=request.POST.get('changePassword')
            cur_user.user_teacher.school=newSchool
            #cur_user.set_password(newPassword)
            cur_user.user_teacher.save()
            cur_user.save()
    if hasattr(cur_user,'user_student'):
        courses=cur_user.user_student.courses.all()
        discusses=cur_user.user_student.student_launch_discuss.all()
        questions=cur_user.user_student.ask_question.all()
    elif hasattr(cur_user,'user_teacher'):
        courses=cur_user.user_teacher.teach_course.all()
        discusses=cur_user.user_teacher.teacher_launch_discuss.all()
        questions={}
    else:
        courses={}
        discusses={}#获取用户的课程及讨论内容
        questions={}
    return render_to_response('profile.html',RequestContext(request,{
        'courses':courses,
        'discusses':discusses,
        'questions':questions,
        }))

@csrf_exempt
def course_page(request,id):
    cur_course=Course.objects.get(pk=id)
    cur_user=request.user
    #判定是否是学生，是否已参加课程，给予不同的权限
    if hasattr(cur_user,'user_student'):
        is_student=True
        if cur_course in cur_user.user_student.courses.all():
            is_attended=True
        else:
            is_attended=False
    else:
        is_student=False
        if cur_course.teacher==cur_user.user_teacher:
            is_attended=True
        else:
            is_attended=False
    print is_student,is_attended
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

@csrf_exempt
def single_discuss_page(request,id):
    cur_discuss=Discuss.objects.get(pk=id)
    if request.method=='POST':
        content=request.POST.get('content')
        cur_reply=Reply(
            content=content,
            author=request.user,
            discuss=cur_discuss
            )
        cur_reply.save()
        cur_discuss.discuss_reply.add(cur_reply)
        cur_discuss.save()
    cur_replys=cur_discuss.discuss_reply.all()
    return render_to_response('single_discuss.html',RequestContext(request,{
        'discuss':cur_discuss,
        'replys':cur_replys,
        }))

@csrf_exempt
def single_question_page(request,id):
    cur_question=Question.objects.get(pk=id)
    if request.method=='POST':
        content=request.POST.get('content')
        cur_reply=Reply(
            content=content,
            author=request.user,
            question=cur_question
            )
        cur_reply.save()
        cur_question.question_reply.add(cur_reply)
        cur_question.save()
    cur_replys=cur_question.question_reply.all()
    return render_to_response('single_question.html',RequestContext(request,{
        'question':cur_question,
        'replys':cur_replys,
        }))

@csrf_exempt
@login_required
def add_new_course_page(request):
    if request.method=='POST':
        name=request.POST.get('name')
        img_url=request.POST.get('img_url')
        cur_course=Course.objects.create(
            name=name,
            img_url=img_url,
            teacher=request.user.user_teacher
            )
        cur_course.save()
        request.user.user_teacher.teach_course.add(cur_course)
        request.user.save()
        return HttpResponseRedirect("/course/%d" % cur_course.id)
    return render_to_response('add_new_course.html',RequestContext(request))