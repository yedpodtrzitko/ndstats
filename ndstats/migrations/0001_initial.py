# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chatlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('message', models.CharField(max_length=255)),
                ('team', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('line', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('map', models.CharField(max_length=20, null=True)),
                ('started', models.DateTimeField(null=True)),
                ('finished', models.DateTimeField(null=True)),
                ('winner', models.PositiveSmallIntegerField(null=True, choices=[(0, b'No team'), (2, b'Consortium'), (3, b'Empire')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buildings', models.PositiveIntegerField(default=0)),
                ('kills', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
                ('res_captured', models.PositiveIntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('team_final', models.PositiveSmallIntegerField(null=True, choices=[(0, b'No team'), (2, b'Consortium'), (3, b'Empire')])),
                ('team_current', models.PositiveSmallIntegerField(null=True, choices=[(0, b'No team'), (2, b'Consortium'), (3, b'Empire')])),
                ('time_empire', models.PositiveIntegerField(default=0)),
                ('time_consortium', models.PositiveIntegerField(default=0)),
                ('time_empire_cmd', models.PositiveIntegerField(default=0)),
                ('timestamp_cmd_change', models.DateTimeField(null=True)),
                ('time_consortium_cmd', models.PositiveIntegerField(default=0)),
                ('commander', models.PositiveSmallIntegerField(null=True, choices=[(0, b'No team'), (2, b'Consortium'), (3, b'Empire')])),
                ('timestamp_last_change', models.DateTimeField(null=True)),
                ('match', models.ForeignKey(to='ndstats.Match')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('nick', models.CharField(max_length=64)),
                ('clantag', models.CharField(max_length=32, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('ip', models.GenericIPAddressField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnknownLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('line', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='matchplayer',
            name='player',
            field=models.ForeignKey(to='ndstats.Player'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='matchplayer',
            unique_together=set([('player', 'match')]),
        ),
        migrations.AddField(
            model_name='match',
            name='server',
            field=models.ForeignKey(to='ndstats.Server'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chatlog',
            name='match',
            field=models.ForeignKey(to='ndstats.Match'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chatlog',
            name='player',
            field=models.ForeignKey(to='ndstats.Player'),
            preserve_default=True,
        ),
    ]

