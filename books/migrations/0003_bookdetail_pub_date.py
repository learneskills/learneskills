# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-25 18:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20170115_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookdetail',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 2, 25, 18, 27, 39, 731620, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
