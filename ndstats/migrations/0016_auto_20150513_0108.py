# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0015_matchevent_entype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchevent',
            options={'ordering': ['when']},
        ),
    ]
