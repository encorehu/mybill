# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0015_auto_20161021_2206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountcategory',
            options={'ordering': ('account', 'tx_type'), 'verbose_name': '\u6536\u652f\u5206\u7c7b', 'verbose_name_plural': '\u6536\u652f\u5206\u7c7b'},
        ),
    ]
