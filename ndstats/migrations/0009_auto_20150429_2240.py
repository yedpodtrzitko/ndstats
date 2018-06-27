# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0008_auto_20150429_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerip',
            name='ip',
            field=models.GenericIPAddressField(db_index=True),
        ),
    ]
