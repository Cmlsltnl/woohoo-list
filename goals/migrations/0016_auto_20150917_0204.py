# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0015_auto_20150916_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepcomment',
            name='author',
            field=models.ForeignKey(to='accounts.GoalSetter', null=True),
        ),
    ]
