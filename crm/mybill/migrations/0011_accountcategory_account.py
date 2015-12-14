# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0010_auto_20151214_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountcategory',
            name='account',
            field=models.ForeignKey(related_name='category_account_set', blank=True, to='mybill.Account', null=True),
        ),
    ]
