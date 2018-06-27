# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0012_auto_20150508_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='map',
            field=models.CharField(max_length=32, blank=True),
        ),
    ]
