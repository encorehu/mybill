# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0020_auto_20160104_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('display_name', models.CharField(default='', max_length=255, null=True, blank=True)),
                ('tx_type', models.IntegerField(default=0, verbose_name='\u6536\u652f\u7c7b\u578b', choices=[(1, '\u6536\u5165'), (0, '\u652f\u51fa')])),
                ('year', models.IntegerField(default=0, verbose_name='\u5e74')),
                ('month', models.IntegerField(default=0, verbose_name='\u6708')),
                ('day', models.IntegerField(default=0, verbose_name='\u65e5')),
                ('level', models.IntegerField(default=0, verbose_name='\u65e5')),
                ('levelname', models.CharField(default='', max_length=32, verbose_name='\u65e5')),
                ('amount', models.DecimalField(default=0.0, verbose_name='\u91d1\u989d', max_digits=10, decimal_places=2)),
                ('account', models.ForeignKey(related_name='stat_account_set', default=None, blank=True, to='mybill.Account', null=True)),
            ],
            options={
                'verbose_name': '\u6536\u652f\u7edf\u8ba1',
                'verbose_name_plural': '\u6536\u652f\u7edf\u8ba1',
            },
        ),
    ]
