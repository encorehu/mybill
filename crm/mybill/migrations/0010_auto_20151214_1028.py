# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0009_accountitem_tx_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ('id',), 'verbose_name': '\u79d1\u76ee\uff08\u8d26\u6237\uff09', 'verbose_name_plural': '\u79d1\u76ee\uff08\u8d26\u6237\uff09'},
        ),
    ]
