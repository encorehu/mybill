# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0013_accountitemdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountitem',
            name='billnum',
            field=models.CharField(default=b'', max_length=32, blank=True),
        ),
    ]
