# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='completion_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='goal',
            name='description',
            field=models.TextField(default=b'Description goes here!'),
        ),
    ]
