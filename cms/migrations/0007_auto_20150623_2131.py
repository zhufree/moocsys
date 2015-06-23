# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20150622_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='studentid',
            field=models.BigIntegerField(unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
