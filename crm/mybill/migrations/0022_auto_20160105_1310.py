# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0021_accountstat'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('debit_symbol', models.IntegerField(default=1, verbose_name='\u7ea7\u522b')),
                ('credit_symbol', models.IntegerField(default=-1, verbose_name='\u7ea7\u522b')),
                ('code', models.CharField(default=b'10', max_length=2, verbose_name='\u4ee3\u7801')),
                ('debit_increase', models.BooleanField(default=True, verbose_name='\u501f\u65b9\u589e\u52a0')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u8d26\u6237\u7c7b\u578b',
                'verbose_name_plural': '\u8d26\u6237\u7c7b\u578b',
            },
        ),
        migrations.AlterField(
            model_name='accountstat',
            name='level',
            field=models.IntegerField(default=0, verbose_name='\u7ea7\u522b'),
        ),
        migrations.AlterField(
            model_name='accountstat',
            name='levelname',
            field=models.CharField(default='', max_length=32, verbose_name='\u7ea7\u522b\u540d\u79f0'),
        ),
    ]
