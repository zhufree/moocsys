#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.
class Teacher(models.Model):
    user=models.OneToOneField(User,related_name="user_teacher")
    school=models.CharField(max_length=200,blank=True)
    def __unicode__(self):
        return u'%s' %(self.user.username)

class Course(models.Model):
    name=models.CharField(max_length=200)
    img_url=models.URLField(default="http://img5.imgtn.bdimg.com/it/u=1547837308,3096775079&fm=21&gp=0.jpg")
    teacher=models.ForeignKey(Teacher,related_name='teach_course',blank=True)#授课教师
    time=models.DateTimeField(auto_now_add=True)#发布时间
    attendance=models.IntegerField(default=0)#参与人数
    def __unicode__(self):
        return u'%s' %(self.name)

class Student(models.Model):
    user=models.OneToOneField(User,related_name="user_student")
    studentid=models.BigIntegerField(unique=True,blank=True,null=True)
    major=models.CharField(max_length=200,blank=True)
    school=models.CharField(max_length=200,blank=True)
    courses=models.ManyToManyField(Course,related_name='course_student',blank=True)#参加的课程
    def __unicode__(self):
        return u'%s' %(self.user.username)

class Discuss(models.Model):
    name=models.CharField(max_length=200,blank=False)
    content=models.CharField(max_length=2000,default='')
    course=models.ForeignKey(Course,related_name='course_discuss',blank=True,null=True)#主题讨论时与之相关的课程
    topic=models.CharField(max_length=200,blank=True)#选题讨论时的主题
    teacher=models.ForeignKey(Teacher,related_name='teacher_launch_discuss',blank=True,null=True)#发起讨论的老师
    student=models.ForeignKey(Student,related_name='student_launch_discuss',blank=True,null=True)#发起讨论的学生
    time=models.DateTimeField(auto_now_add=True)#发起时间
    def __unicode__(self):
        return u'%s' %(self.name)

class Question(models.Model):
    title=models.CharField(max_length=200,blank=False)
    content=models.CharField(max_length=1000,default='')
    course=models.ForeignKey(Course,related_name='course_question',blank=True,null=True)
    quizzer=models.ForeignKey(Student,related_name='ask_question')#问题发起者
    teacher_answer=models.ForeignKey(Teacher,related_name='teacher_answer_question',blank=True,null=True)#教师的回答
    student_answer=models.ForeignKey(Student,related_name='student_answer_question',blank=True,null=True)#学生的回答
    time=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' %(self.title)
class Reply(models.Model):
    content=models.CharField(max_length=5000,default='')
    author=models.ForeignKey(User,related_name='user_reply')
    discuss=models.ForeignKey(Discuss,related_name='discuss_reply',blank=True,null=True)
    question=models.ForeignKey(Question,related_name='question_reply',blank=True,null=True)
    time=models.DateTimeField(auto_now_add=True)

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Discuss)
admin.site.register(Question)
admin.site.register(Reply)