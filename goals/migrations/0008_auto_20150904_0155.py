# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0007_step_step_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='detail',
            field=models.CharField(default=b'Take one step closer!', max_length=256),
        ),
    ]
