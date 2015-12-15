# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mybill', '0012_auto_20151214_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountItemDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('summary', models.CharField(default='\u9910\u8d39', max_length=255, null=True, blank=True)),
                ('amount', models.DecimalField(default=0.0, verbose_name='\u91d1\u989d', max_digits=10, decimal_places=2)),
                ('tx_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4ea4\u6613\u65e5\u671f')),
                ('tx_type', models.IntegerField(default=0, verbose_name='\u6536\u652f\u7c7b\u578b', choices=[(1, '\u6536\u5165'), (0, '\u652f\u51fa')])),
                ('operator', models.CharField(default=b'hcz', max_length=20, editable=False)),
                ('accountitem', models.ForeignKey(related_name='accountitem_set', to='mybill.AccountItem')),
            ],
            options={
                'ordering': ('tx_date', 'id'),
                'verbose_name': '\u8bb0\u8d26\u6761\u76ee\u660e\u7ec6',
                'verbose_name_plural': '\u8bb0\u8d26\u6761\u76ee\u660e\u7ec6',
            },
        ),
    ]
