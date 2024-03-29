# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-18 00:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0018_remove_tweet9_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(upload_to='file')),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('total_likes', models.PositiveIntegerField(db_index=True, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_created', to=settings.AUTH_USER_MODEL)),
                ('users_like', models.ManyToManyField(blank=True, related_name='event_liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
