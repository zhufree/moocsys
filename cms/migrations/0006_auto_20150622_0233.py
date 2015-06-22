# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20150622_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='major',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='studentid',
            field=models.BigIntegerField(unique=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='teacher',
            name='school',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
