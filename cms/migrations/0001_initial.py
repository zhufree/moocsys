# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('img_url', models.URLField(default=b'http://img5.imgtn.bdimg.com/it/u=1547837308,3096775079&fm=21&gp=0.jpg')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('attendance', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Discuss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('content', models.CharField(default=b'', max_length=2000)),
                ('topic', models.CharField(max_length=200, blank=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(related_name='course_discuss', blank=True, to='cms.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.CharField(default=b'', max_length=1000)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(related_name='course_question', blank=True, to='cms.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'', max_length=5000)),
                ('author', models.ForeignKey(related_name='user_reply', to=settings.AUTH_USER_MODEL)),
                ('discuss', models.ForeignKey(related_name='discuss_reply', blank=True, to='cms.Discuss')),
                ('question', models.ForeignKey(related_name='question_reply', blank=True, to='cms.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentid', models.BigIntegerField(unique=True)),
                ('major', models.CharField(max_length=200)),
                ('school', models.CharField(max_length=200)),
                ('courses', models.ManyToManyField(related_name='course_student', to='cms.Course', blank=True)),
                ('user', models.OneToOneField(related_name='user_student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('school', models.CharField(max_length=200)),
                ('user', models.OneToOneField(related_name='user_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='quizzer',
            field=models.ForeignKey(related_name='ask_question', to='cms.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='student_answer',
            field=models.ForeignKey(related_name='student_answer_question', blank=True, to='cms.Student', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='teacher_answer',
            field=models.ForeignKey(related_name='teacher_answer_question', blank=True, to='cms.Teacher', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discuss',
            name='student',
            field=models.ForeignKey(related_name='student_launch_discuss', blank=True, to='cms.Student', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discuss',
            name='teacher',
            field=models.ForeignKey(related_name='teacher_launch_discuss', blank=True, to='cms.Teacher', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(related_name='teach_course', blank=True, to='cms.Teacher'),
            preserve_default=True,
        ),
    ]
