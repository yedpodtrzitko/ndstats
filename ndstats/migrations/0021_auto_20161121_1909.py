# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0020_foodproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodproduct',
            name='is_available',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='foodproduct',
            name='picture',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
