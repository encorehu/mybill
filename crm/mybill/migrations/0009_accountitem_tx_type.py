# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0008_accountitem_category_verbosename'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountitem',
            name='tx_type',
            field=models.IntegerField(default=0, verbose_name='\u6536\u652f\u7c7b\u578b', choices=[(1, '\u6536\u5165'), (0, '\u652f\u51fa')]),
        ),
    ]
