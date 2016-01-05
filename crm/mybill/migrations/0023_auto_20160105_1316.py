# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0022_auto_20160105_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='credit_symbol',
            field=models.CharField(default=b'-', max_length=1, verbose_name='\u8d37\u65b9\u7b26\u53f7', choices=[(b'+', '\u501f\u65b9\u7b26\u53f7'), (b'-', '\u8d37\u65b9\u7b26\u53f7')]),
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='debit_symbol',
            field=models.CharField(default=b'+', max_length=1, verbose_name='\u501f\u65b9\u7b26\u53f7', choices=[(b'+', '\u501f\u65b9\u7b26\u53f7'), (b'-', '\u8d37\u65b9\u7b26\u53f7')]),
        ),
    ]
