# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0015_auto_20151215_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True, blank=True)),
                ('balance', models.DecimalField(default=0.0, verbose_name='\u91d1\u989d', max_digits=10, decimal_places=2)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u8d26\u672c',
                'verbose_name_plural': '\u8d26\u672c',
            },
        ),
    ]
