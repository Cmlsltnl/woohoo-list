# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_friendship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='friend_users',
            field=models.ForeignKey(related_name='friends', to='accounts.GoalSetter', null=True),
        ),
    ]
