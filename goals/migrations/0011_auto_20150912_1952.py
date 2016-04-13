# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0010_auto_20150904_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='description',
            field=models.TextField(),
        ),
    ]
