# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-08-24 15:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bussiness', '0002_auto_20190822_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bussiness2',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bussiness', to=settings.AUTH_USER_MODEL),
        ),
    ]
