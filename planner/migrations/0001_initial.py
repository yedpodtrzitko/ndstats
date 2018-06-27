# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0002_auto_20141210_0103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when', models.DateTimeField(verbose_name='Event datetime')),
                ('rounds', models.PositiveIntegerField(default=2, verbose_name='No of rounds')),
            ],
            options={
                'ordering': ('when',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='planner.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='Name of the map')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=3, verbose_name='Status', choices=[(b'com', 'Commander'), (b'yes', 'Player'), (b'may', '?'), (b'no', 'No')])),
                ('event', models.ForeignKey(to='planner.Event')),
                ('maps', models.ManyToManyField(to='planner.Map', through='planner.EventMap')),
                ('player', models.ForeignKey(to='default.UserSocialAuth')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='participant',
            unique_together=set([('player', 'event')]),
        ),
        migrations.AddField(
            model_name='eventmap',
            name='map',
            field=models.ForeignKey(to='planner.Map'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventmap',
            name='participant',
            field=models.ForeignKey(to='planner.Participant'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='eventmap',
            unique_together=set([('participant', 'map', 'event')]),
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(to='default.UserSocialAuth', through='planner.Participant'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UserSocialAuthProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Steam login',
                'proxy': True,
            },
            bases=('default.usersocialauth',),
        ),
    ]
