# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20150621_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discuss',
            name='course',
            field=models.ForeignKey(related_name='course_discuss', blank=True, to='cms.Course', null=True),
            preserve_default=True,
        ),
    ]
