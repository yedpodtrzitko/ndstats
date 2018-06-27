# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0013_server_map'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchevent',
            name='entity',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='matchevent',
            name='what',
            field=models.IntegerField(choices=[(0, b'death'), (1, b'destroyed'), (2, b'built')]),
        ),
    ]
