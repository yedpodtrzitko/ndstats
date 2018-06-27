# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0006_server_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='port',
            field=models.PositiveIntegerField(default=27015),
            preserve_default=True,
        ),
    ]
