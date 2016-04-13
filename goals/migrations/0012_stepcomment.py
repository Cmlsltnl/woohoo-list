# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150904_0328'),
        ('goals', '0011_auto_20150912_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='StepComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(null=True)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='accounts.GoalSetter')),
                ('comment_step', models.ForeignKey(related_name='comments', to='goals.Step', null=True)),
            ],
        ),
    ]
