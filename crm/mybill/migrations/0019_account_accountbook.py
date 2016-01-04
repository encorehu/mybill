# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0018_remove_accountbook_accounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='accountbook',
            field=models.ForeignKey(related_name='account_book_set', default=None, blank=True, to='mybill.AccountBook', null=True),
        ),
    ]
