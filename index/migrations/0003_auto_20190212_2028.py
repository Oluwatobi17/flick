# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-12 19:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_following_profilepicture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilepicture',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profilepicture',
        ),
    ]
