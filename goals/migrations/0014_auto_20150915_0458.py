# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0013_step_completed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='completed_date',
            field=models.DateField(null=True),
        ),
    ]
