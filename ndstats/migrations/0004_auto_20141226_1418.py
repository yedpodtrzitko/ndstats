# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0003_auto_20141226_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatlog',
            name='team',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'Spectator'), (1, b'Consortium'), (2, b'Empire')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'Spectator'), (1, b'Consortium'), (2, b'Empire')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='matchplayer',
            name='commander',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'Spectator'), (1, b'Consortium'), (2, b'Empire')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='matchplayer',
            name='team_current',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'Spectator'), (1, b'Consortium'), (2, b'Empire')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='matchplayer',
            name='team_final',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'Spectator'), (1, b'Consortium'), (2, b'Empire')]),
            preserve_default=True,
        ),
    ]
