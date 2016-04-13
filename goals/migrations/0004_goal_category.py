# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_goal_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='category',
            field=models.CharField(max_length=3, null=True, choices=[(b'FIN', b'Finance'), (b'FIT', b'Fitness'), (b'LEA', b'Learning'), (b'PER', b'Personal')]),
        ),
    ]
