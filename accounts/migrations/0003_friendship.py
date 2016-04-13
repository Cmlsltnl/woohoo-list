# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150904_0328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('friend_users', models.ForeignKey(related_name='friends', to='accounts.GoalSetter')),
                ('main_user', models.ForeignKey(to='accounts.GoalSetter')),
            ],
        ),
    ]
