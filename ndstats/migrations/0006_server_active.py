# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0005_auto_20141226_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
