# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0021_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=16)),
                ('name', models.CharField(default=b'', max_length=32)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, blank=True, null=True, verbose_name='\u8d26\u672c\u91d1\u989d\u5408\u8ba1')),
            ],
            options={
                'ordering': ('code', 'id'),
                'verbose_name': '\u8d26\u672c',
                'verbose_name_plural': '\u8d26\u672c',
            },
        ),
    ]
