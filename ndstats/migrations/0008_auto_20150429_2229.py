# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0007_server_port'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['-started'], 'verbose_name_plural': 'Matches'},
        ),
        migrations.AddField(
            model_name='match',
            name='crashed',
            field=models.BooleanField(default=False),
        ),
    ]
