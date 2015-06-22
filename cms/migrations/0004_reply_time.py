# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20150621_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 21, 16, 19, 52, 977000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
