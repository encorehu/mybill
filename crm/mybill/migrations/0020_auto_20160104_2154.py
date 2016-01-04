# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0019_account_accountbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountbook',
            name='balance_cash',
            field=models.DecimalField(default=0.0, verbose_name='\u73b0\u91d1', max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='accountbook',
            name='balance_deposit',
            field=models.DecimalField(default=0.0, verbose_name='\u5b58\u6b3e', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='accountbook',
            name='balance',
            field=models.DecimalField(default=0.0, verbose_name='\u4f59\u989d', max_digits=10, decimal_places=2),
        ),
    ]
