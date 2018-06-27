# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndstats', '0002_auto_20141226_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerNick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(max_length=64)),
                ('changed', models.DateTimeField(auto_now_add=True)),
                ('player', models.ForeignKey(to='ndstats.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['-started']},
        ),
        migrations.AddField(
            model_name='player',
            name='nick_history',
            field=models.ManyToManyField(related_name='nick_history', to='ndstats.PlayerNick'),
            preserve_default=True,
        ),
    ]
