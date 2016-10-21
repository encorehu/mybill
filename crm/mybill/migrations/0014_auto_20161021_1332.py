# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0013_auto_20161017_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountitem',
            name='category',
            field=models.ForeignKey(related_name='account_category_item_set', to='mybill.AccountCategory', null=True),
        ),
    ]
