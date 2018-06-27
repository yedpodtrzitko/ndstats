# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0016_auto_20150513_0108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='crashed',
        ),
    ]
