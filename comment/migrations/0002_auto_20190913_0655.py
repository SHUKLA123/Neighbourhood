# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-09-13 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='url',
        ),
        migrations.AddField(
            model_name='comments',
            name='pincode',
            field=models.CharField(default=121004, max_length=6),
            preserve_default=False,
        ),
    ]
