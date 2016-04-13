# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0006_auto_20150903_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='step_number',
            field=models.IntegerField(default=1),
        ),
    ]
