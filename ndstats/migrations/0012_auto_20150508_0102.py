# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0011_matchevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchevent',
            name='team',
            field=models.PositiveSmallIntegerField(choices=[(0, b'UNASSIGNED'), (1, b'CONSORTIUM'), (2, b'EMPIRE')]),
        ),
    ]
