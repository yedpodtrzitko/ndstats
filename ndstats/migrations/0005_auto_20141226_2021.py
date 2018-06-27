# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0004_auto_20141226_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerIP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('when', models.DateTimeField()),
                ('player', models.ForeignKey(to='ndstats.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='playerip',
            unique_together=set([('player', 'ip')]),
        ),
        migrations.AddField(
            model_name='player',
            name='ip_history',
            field=models.ManyToManyField(related_name='ip_history', to='ndstats.PlayerIP'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chatlog',
            name='team',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'UNASSIGNED'), (1, b'CONSORTIUM'), (2, b'EMPIRE')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'UNASSIGNED'), (1, b'CONSORTIUM'), (2, b'EMPIRE')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='matchplayer',
            name='commander',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'UNASSIGNED'), (1, b'CONSORTIUM'), (2, b'EMPIRE')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='matchplayer',
            name='team_current',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'UNASSIGNED'), (1, b'CONSORTIUM'), (2, b'EMPIRE')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='matchplayer',
            name='team_final',
            field=models.PositiveSmallIntegerField(null=True, choices=[(0, b'UNASSIGNED'), (1, b'CONSORTIUM'), (2, b'EMPIRE')]),
            preserve_default=True,
        ),
    ]
