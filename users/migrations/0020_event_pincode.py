# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-18 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='pincode',
            field=models.CharField(default=121004, max_length=6),
            preserve_default=False,
        ),
    ]
