# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0011_auto_20160406_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountcategory',
            name='account',
            field=models.ForeignKey(related_name='category_account_set', default=None, blank=True, to='mybill.Account', null=True),
        ),
    ]
