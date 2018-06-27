# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatlog',
            old_name='team',
            new_name='private',
        ),
        migrations.AddField(
            model_name='chatlog',
            name='team',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'No team'), (2, b'Consortium'), (3, b'Empire')]),
            preserve_default=True,
        ),
    ]
