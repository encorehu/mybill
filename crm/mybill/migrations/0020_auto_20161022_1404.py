# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0019_auto_20161022_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountitem',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, blank=True, null=True, verbose_name='\u4f59\u989d'),
        ),
    ]
