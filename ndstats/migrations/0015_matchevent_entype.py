# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0014_auto_20150509_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchevent',
            name='entype',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
