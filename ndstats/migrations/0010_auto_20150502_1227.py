# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0009_auto_20150429_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='score',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='score_saved',
            field=models.IntegerField(default=0),
        ),
    ]
