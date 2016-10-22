# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0016_auto_20161022_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountitem',
            name='balance',
            field=models.DecimalField(default=0.0, verbose_name='\u4f59\u989d', max_digits=10, decimal_places=2),
        ),
    ]
