# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0004_remove_accountitem_debit'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountitem',
            name='amount',
            field=models.DecimalField(default=0.0, verbose_name='\u91d1\u989d', max_digits=10, decimal_places=2),
        ),
    ]
