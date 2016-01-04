# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0016_accountbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountbook',
            name='accounts',
            field=models.ManyToManyField(to='mybill.Account'),
        ),
    ]
