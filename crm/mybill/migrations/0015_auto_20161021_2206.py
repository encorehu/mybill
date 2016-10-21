# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0014_auto_20161021_1332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountcategory',
            options={'ordering': ('account',), 'verbose_name': '\u6536\u652f\u5206\u7c7b', 'verbose_name_plural': '\u6536\u652f\u5206\u7c7b'},
        ),
    ]
