# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0008_auto_20150904_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='step_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
