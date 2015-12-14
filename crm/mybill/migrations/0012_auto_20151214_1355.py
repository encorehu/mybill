# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0011_accountcategory_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountcategory',
            name='account',
            field=models.ForeignKey(related_name='category_account_set', default=None, blank=True, to='mybill.Account', null=True),
        ),
    ]
