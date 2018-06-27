# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0010_auto_20150502_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when', models.DateTimeField()),
                ('what', models.IntegerField(choices=[(0, b'death'), (1, b'destroyed')])),
                ('team', models.PositiveSmallIntegerField()),
                ('where_x', models.IntegerField()),
                ('where_y', models.IntegerField()),
                ('where_z', models.IntegerField()),
                ('match', models.ForeignKey(to='ndstats.Match')),
            ],
        ),
    ]
