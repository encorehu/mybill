# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0010_accountitem_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(default=b'', max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='display_name',
            field=models.CharField(default=b'', max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(default=b'', max_length=20, null=True, blank=True),
        ),
    ]
