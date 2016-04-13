# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0005_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='step',
            name='parent_goal',
            field=models.ForeignKey(related_name='steps', blank=True, to='goals.Goal', null=True),
        ),
    ]
