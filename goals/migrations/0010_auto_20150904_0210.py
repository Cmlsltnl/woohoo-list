# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0009_auto_20150904_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='creator',
            field=models.ForeignKey(to='accounts.GoalSetter', null=True),
        ),
    ]
