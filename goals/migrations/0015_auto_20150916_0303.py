# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0014_auto_20150915_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='completed_date',
            field=models.DateTimeField(null=True),
        ),
    ]
