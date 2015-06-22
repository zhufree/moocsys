# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_reply_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='discuss',
            field=models.ForeignKey(related_name='discuss_reply', blank=True, to='cms.Discuss', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reply',
            name='question',
            field=models.ForeignKey(related_name='question_reply', blank=True, to='cms.Question', null=True),
            preserve_default=True,
        ),
    ]
