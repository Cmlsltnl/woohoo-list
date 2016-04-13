# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0004_goal_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('detail', models.CharField(default=b'One step closer!', max_length=256)),
                ('target_date', models.DateField(default=datetime.date.today)),
                ('completed', models.BooleanField(default=False)),
                ('parent_goal', models.ForeignKey(to='goals.Goal', null=True)),
            ],
        ),
    ]
