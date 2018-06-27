# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0017_remove_match_crashed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchevent',
            name='entity',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
