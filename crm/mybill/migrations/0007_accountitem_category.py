# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0006_auto_20151130_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountitem',
            name='category',
            field=models.ForeignKey(related_name='account_category_item_set', default=1, to='mybill.AccountCategory'),
            preserve_default=False,
        ),
    ]
