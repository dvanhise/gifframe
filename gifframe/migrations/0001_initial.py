# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cachable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('link', models.URLField()),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('image', models.CharField(max_length=200)),
                ('order', models.IntegerField()),
                ('gif', models.ForeignKey(to='gifframe.Cachable')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='frame',
            unique_together=set([('order', 'gif')]),
        ),
    ]
