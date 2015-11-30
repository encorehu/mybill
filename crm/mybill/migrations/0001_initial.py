# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=20)),
                ('account_type', models.CharField(max_length=10, null=True, blank=True)),
                ('name', models.CharField(max_length=20, null=True, blank=True)),
                ('display_name', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u79d1\u76ee\uff08\u8d26\u6237\uff09',
                'verbose_name_plural': '\u79d1\u76ee\uff08\u8d26\u6237\uff09',
            },
        ),
        migrations.CreateModel(
            name='AccountItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='', max_length=255, null=True, blank=True)),
                ('summary', models.CharField(default='\u9910\u8d39', max_length=255, null=True, blank=True)),
                ('debit', models.DecimalField(default=0.0, verbose_name='\u6536\u5165', max_digits=10, decimal_places=2)),
                ('credit', models.DecimalField(default=0.0, verbose_name='\u652f\u51fa', max_digits=10, decimal_places=2)),
                ('balance', models.DecimalField(default=0.0, verbose_name='\u4f59\u989d', max_digits=10, decimal_places=2)),
                ('tx_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4ea4\u6613\u65e5\u671f')),
                ('adding_type', models.IntegerField(default=0, editable=False)),
                ('adding_type_name', models.CharField(default=b'manual', max_length=20, editable=False)),
                ('operator', models.CharField(default=b'hcz', max_length=20, editable=False)),
                ('transaction_id', models.IntegerField(default=0, editable=False)),
                ('account', models.ForeignKey(related_name='account_set', to='mybill.Account')),
            ],
            options={
                'ordering': ('tx_date',),
                'verbose_name': '\u8bb0\u8d26\u6761\u76ee',
                'verbose_name_plural': '\u8bb0\u8d26\u6761\u76ee',
            },
        ),
    ]
