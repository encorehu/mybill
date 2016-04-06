# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0009_accountitem_tx_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountitem',
            name='receipt',
            field=models.CharField(default='', max_length=32, null=True, verbose_name='\u7968\u636e\u53f7\u7801', blank=True),
        ),
    ]
