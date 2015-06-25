# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('unique_id', models.CharField(unique=True, max_length=40)),
                ('code', models.CharField(max_length=2000)),
                ('cf_submission_id', models.IntegerField()),
                ('cf_verdict', models.IntegerField()),
                ('cf_verdict_details', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('cf_contest_id', models.IntegerField()),
                ('cf_problem_index', models.CharField(max_length=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='attempt',
            name='exercise',
            field=models.ForeignKey(to='cpe.Exercise'),
            preserve_default=True,
        ),
    ]
