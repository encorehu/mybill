# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0002_remove_accountitem_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountitem',
            name='credit',
        ),
    ]
