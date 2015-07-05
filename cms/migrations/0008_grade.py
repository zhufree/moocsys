# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20150623_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mark', models.IntegerField(default=0)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(related_name='course_grade', to='cms.Course')),
                ('student', models.ForeignKey(related_name='student_grade', to='cms.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
