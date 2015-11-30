# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0007_accountitem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountitem',
            name='category_verbosename',
            field=models.CharField(default='', max_length=255, null=True, blank=True),
        ),
    ]
