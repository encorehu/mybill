# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0014_accountitem_billnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountitem',
            name='billnum',
            field=models.CharField(default=b'', max_length=32, verbose_name='\u7968\u636e\u53f7\u7801', blank=True),
        ),
    ]
