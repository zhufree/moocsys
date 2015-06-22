# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='course',
            field=models.ForeignKey(related_name='course_question', blank=True, to='cms.Course', null=True),
            preserve_default=True,
        ),
    ]
