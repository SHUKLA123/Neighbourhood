# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-09-10 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20190910_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
