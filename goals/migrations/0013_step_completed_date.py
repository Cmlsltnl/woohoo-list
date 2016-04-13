# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0012_stepcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='completed_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
